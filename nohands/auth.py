"""
No Hands 2FA Handler
====================
Handles two-factor authentication flows gracefully.
Notifies via Telegram, waits for manual entry, or auto-enters code.
"""

import asyncio
import time


class TwoFactorHandler:
    """Handle 2FA flows across any platform."""

    def __init__(self, nh):
        self.nh = nh

    async def handle(
        self,
        code: str = None,
        wait_timeout: int = 120,
        notify_telegram: bool = True,
    ) -> bool:
        """
        Handle a 2FA challenge.

        If code is provided, enters it immediately.
        Otherwise, detects the 2FA type and waits.
        """

        # Detect 2FA type from page content
        page_text = await self.nh.get_page_text(1000)
        lower = page_text.lower()

        is_2fa = any(kw in lower for kw in [
            "verification", "two-factor", "2fa", "two factor",
            "authentication code", "verify your identity",
            "enter the code", "security code", "one-time",
            "authenticator", "sms code", "check your device",
        ])

        if not is_2fa:
            # Check URL
            url = self.nh.page.url.lower()
            is_2fa = any(kw in url for kw in [
                "checkpoint", "two_step", "two-factor", "verify", "auth"
            ])

        if not is_2fa:
            self.nh._log("No 2FA detected on page", "info")
            return True

        self.nh._log("2FA detected!", "warn")
        await self.nh.screenshot("2fa_detected")

        # Notify via Telegram
        if notify_telegram:
            await self.nh.notify(
                f"⚠️ 2FA Required!\n\n"
                f"URL: {self.nh.page.url}\n"
                f"Page says: {page_text[:200]}\n\n"
                f"Please complete 2FA or provide the code."
            )

        # If code provided, try to enter it
        if code:
            return await self._enter_code(code)

        # Wait for manual completion
        self.nh._log(f"Waiting up to {wait_timeout}s for 2FA completion...", "info")
        start = time.time()

        while time.time() - start < wait_timeout:
            # Check if page changed (2FA completed)
            current_text = await self.nh.get_page_text(500)
            current_lower = current_text.lower()
            current_url = self.nh.page.url.lower()

            # Detect completion
            no_longer_2fa = not any(kw in current_lower for kw in [
                "verification", "two-factor", "enter the code",
                "security code", "authenticator",
            ]) and not any(kw in current_url for kw in [
                "checkpoint", "two_step", "verify",
            ])

            if no_longer_2fa:
                self.nh._log("2FA completed!", "success")
                if notify_telegram:
                    await self.nh.notify("✅ 2FA completed!")
                return True

            await asyncio.sleep(2)

        self.nh._log("2FA timeout — not completed", "error")
        return False

    async def _enter_code(self, code: str) -> bool:
        """Enter a 2FA code into the appropriate field."""
        # Try common 2FA input selectors
        selectors = [
            'input[name="code"]',
            'input[name="verificationCode"]',
            'input[name="totp"]',
            'input[name="otp"]',
            'input[id="code"]',
            'input[type="tel"]',
            'input[autocomplete="one-time-code"]',
            'input[inputmode="numeric"]',
        ]

        for sel in selectors:
            el = await self.nh.page.query_selector(sel)
            if el and await el.is_visible():
                await el.fill(code)
                self.nh._log(f"2FA code entered via {sel}", "success")

                # Try to submit
                await self.nh.page.keyboard.press("Enter")
                await asyncio.sleep(3)
                return True

        # Fallback: try filling any visible input
        return await self.nh.smart_fill("code", code)
