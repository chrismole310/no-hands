"""
No Hands — TikTok Platform Module
===================================
Handles TikTok Studio upload, caption, privacy, and posting.
Battles: content check modals, "Got it" popups, privacy defaults.
"""

import asyncio


class TikTokPoster:
    """Post videos to TikTok via TikTok Studio."""

    def __init__(self, nh):
        self.nh = nh

    async def post(self, video_path: str, caption: str, privacy: str = "Everyone") -> bool:
        """
        Full TikTok posting flow:
        1. Navigate to TikTok Studio upload
        2. Upload video
        3. Dismiss all modals (content check, "Got it", etc.)
        4. Fill caption with hashtags
        5. Set privacy
        6. Click Post
        7. Verify
        """
        nh = self.nh

        # Step 1: Navigate
        nh._log("TikTok: Starting upload flow")
        await nh.goto("https://www.tiktok.com/tiktokstudio/upload?lang=en")
        await asyncio.sleep(3)

        # Check login
        if "login" in nh.page.url:
            nh._log("TikTok: Not logged in!", "error")
            return False

        # Step 2: Upload video
        uploaded = await nh.upload_file(video_path)
        if not uploaded:
            nh._log("TikTok: Upload failed", "error")
            return False

        nh._log("TikTok: Video uploading...")
        await asyncio.sleep(12)

        # Step 3: Dismiss ALL modals (the TikTok special)
        for _ in range(5):
            await nh.dismiss_modals()
            await asyncio.sleep(1)

        # Step 4: Fill caption
        editables = await nh.page.query_selector_all('div[contenteditable="true"]')
        filled = False
        for el in editables:
            try:
                if await el.is_visible():
                    box = await el.bounding_box()
                    if box and box["height"] > 10:
                        await el.click(force=True)
                        await asyncio.sleep(0.3)
                        await nh.page.keyboard.press("Meta+a")
                        await nh.page.keyboard.press("Backspace")
                        await asyncio.sleep(0.2)
                        await nh.page.keyboard.type(caption, delay=3)
                        filled = True
                        nh._log("TikTok: Caption filled", "success")
                        break
            except Exception:
                continue

        if not filled:
            nh._log("TikTok: Could not fill caption", "warn")

        await asyncio.sleep(1)
        await nh.dismiss_modals()

        # Step 5: Scroll and post
        await nh.page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
        await asyncio.sleep(2)
        await nh.dismiss_modals()

        # Step 6: Click Post (with retry for modal interference)
        posted = False
        for attempt in range(3):
            await nh.dismiss_modals()
            await asyncio.sleep(0.5)

            result = await nh.smart_click("Post", force=True)
            if result:
                posted = True
                break
            await asyncio.sleep(2)

        if not posted:
            # JavaScript fallback
            posted = await nh.page.evaluate("""() => {
                const btns = document.querySelectorAll('button');
                for (const b of btns) {
                    if (b.textContent.trim() === 'Post' && !b.disabled) {
                        b.click(); return true;
                    }
                }
                return false;
            }""")

        # Step 7: Verify
        await asyncio.sleep(15)
        await nh.goto("https://www.tiktok.com/tiktokstudio/content")
        await asyncio.sleep(5)

        body = await nh.get_page_text(500)
        if "No posts yet" not in body:
            nh._log("TikTok: POST SUCCESSFUL!", "success")
            return True
        else:
            nh._log("TikTok: Post may not have gone through", "warn")
            return False
