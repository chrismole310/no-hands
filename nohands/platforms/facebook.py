"""No Hands — Facebook Platform Module"""
import asyncio

class FacebookPoster:
    def __init__(self, nh): self.nh = nh

    async def post_to_page(self, page_url, text, video_path=None):
        nh = self.nh
        await nh.goto(page_url)
        await asyncio.sleep(5)
        await nh.dismiss_modals()

        # Click composer
        await nh.smart_click("What's on your mind", force=True)
        await asyncio.sleep(2)

        if text:
            editor = await nh.smart_find(role="textbox")
            if editor and not isinstance(editor, dict):
                await editor.click()
                await nh.page.keyboard.type(text, delay=5)

        if video_path:
            await nh.smart_click("Photo/video")
            await asyncio.sleep(1)
            await nh.upload_file(video_path)
            await asyncio.sleep(10)

        await nh.smart_click("Post")
        await asyncio.sleep(10)
        nh._log("Facebook: POSTED!", "success")
        return True
