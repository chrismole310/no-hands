"""No Hands — Instagram Platform Module"""
import asyncio

class InstagramPoster:
    def __init__(self, nh): self.nh = nh

    async def post_reel(self, video_path, caption):
        nh = self.nh
        await nh.goto("https://www.instagram.com/")
        await asyncio.sleep(5)
        await nh.dismiss_modals()
        if "login" in nh.page.url: return False

        # Click Create > Post
        for link in await nh.page.query_selector_all('a'):
            txt = (await link.text_content() or '').strip()
            if 'Create' in txt:
                await link.click(); await asyncio.sleep(2); break

        await nh.smart_click("Post")
        await asyncio.sleep(3)
        if not await nh.upload_file(video_path): return False
        await asyncio.sleep(8)

        # Handle "Video posts are now shared as reels" modal
        await nh.smart_click("OK")
        await asyncio.sleep(2)

        # Next through crop/edit
        for _ in range(2):
            await nh.smart_click("Next")
            await asyncio.sleep(3)

        # Caption
        for el in await nh.page.query_selector_all('textarea, [contenteditable="true"], [role="textbox"]'):
            if await el.is_visible():
                await el.click()
                await nh.page.keyboard.type(caption, delay=3)
                break

        await asyncio.sleep(1)
        await nh.smart_click("Share")
        await asyncio.sleep(20)
        nh._log("Instagram: POSTED!", "success")
        return True
