"""
No Hands Deep Navigator
=======================
Click → wait → screenshot → analyze → click next → repeat.
Goes 10+ levels deep without losing track.
"""

import asyncio
from typing import List, Dict, Any


class DeepNavigator:
    """
    Navigate through multi-step flows with screenshot verification at each step.

    Example:
        steps = [
            {"action": "click", "target": "Create App"},
            {"action": "click", "target": "Other"},
            {"action": "click", "target": "Next"},
            {"action": "fill", "target": "App name", "value": "My App"},
            {"action": "fill", "target": "email", "value": "me@example.com"},
            {"action": "click", "target": "Create"},
            {"action": "wait_for_text", "target": "App created successfully"},
        ]
        await nh.deep_navigate(steps)
    """

    def __init__(self, nh):
        self.nh = nh

    async def execute(self, steps: List[Dict[str, Any]], screenshot_each: bool = True) -> bool:
        """Execute a sequence of navigation steps."""
        total = len(steps)
        self.nh._log(f"Deep navigation: {total} steps")

        for i, step in enumerate(steps):
            action = step.get("action", "click")
            target = step.get("target", "")
            value = step.get("value", "")
            wait = step.get("wait", None)
            force = step.get("force", False)

            self.nh._log(f"Step {i+1}/{total}: {action} → {target}")

            success = False

            if action == "click":
                success = await self.nh.smart_click(
                    text=target, force=force,
                    wait_after=wait or 2.0
                )

            elif action == "click_selector":
                success = await self.nh.smart_click(
                    selector=target, force=force,
                    wait_after=wait or 2.0
                )

            elif action == "fill":
                success = await self.nh.smart_fill(target, value)

            elif action == "wait":
                await asyncio.sleep(float(target or wait or 3))
                success = True

            elif action == "wait_for_text":
                success = await self.nh.wait_for_text(target, timeout=float(wait or 30))

            elif action == "wait_for_url":
                success = await self.nh.wait_for_url(target, timeout=float(wait or 30))

            elif action == "screenshot":
                await self.nh.screenshot(target or f"step_{i+1}")
                success = True

            elif action == "dismiss_modals":
                await self.nh.dismiss_modals()
                success = True

            elif action == "upload":
                success = await self.nh.upload_file(target)

            elif action == "press":
                await self.nh.page.keyboard.press(target)
                success = True

            elif action == "goto":
                await self.nh.goto(target)
                success = True

            elif action == "scroll_down":
                await self.nh.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await asyncio.sleep(1)
                success = True

            elif action == "handle_2fa":
                success = await self.nh.handle_2fa(code=value if value else None)

            else:
                self.nh._log(f"Unknown action: {action}", "error")
                continue

            # Screenshot after each step
            if screenshot_each:
                await self.nh.screenshot(f"deep_{i+1:02d}_{action}")

            # Human pause between steps
            await self.nh.human_pause()

            if not success:
                # Check if step is required
                if step.get("required", True):
                    self.nh._log(f"Step {i+1} failed — stopping navigation", "error")
                    return False
                else:
                    self.nh._log(f"Step {i+1} failed — optional, continuing", "warn")

        self.nh._log(f"Deep navigation complete: {total} steps", "success")
        return True
