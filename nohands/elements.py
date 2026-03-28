"""
No Hands Smart Elements
=======================
Enhanced element interaction with built-in retry and fallback.
"""


class SmartElement:
    """Wrapper around Playwright elements with smart behavior."""

    def __init__(self, element, nh):
        self.element = element
        self.nh = nh

    async def click(self, force=False, retries=3):
        """Click with retry and force fallback."""
        for attempt in range(retries):
            try:
                await self.element.scroll_into_view_if_needed()
                if force:
                    await self.element.click(force=True)
                else:
                    await self.element.click(timeout=5000)
                return True
            except Exception:
                if attempt == retries - 1:
                    try:
                        await self.element.click(force=True)
                        return True
                    except Exception:
                        return False
                await self.nh.human_pause()
        return False

    async def fill(self, value, clear=True):
        """Fill with clear and keyboard fallback."""
        try:
            if clear:
                await self.element.click(force=True)
                await self.nh.page.keyboard.press("Meta+a")
                await self.nh.page.keyboard.press("Backspace")

            await self.nh.page.keyboard.type(value, delay=self.nh.typing_delay)
            return True
        except Exception:
            try:
                await self.element.fill(value)
                return True
            except Exception:
                return False

    async def text(self):
        """Get text content."""
        return (await self.element.text_content() or "").strip()

    async def is_visible(self):
        """Check visibility."""
        try:
            return await self.element.is_visible()
        except Exception:
            return False
