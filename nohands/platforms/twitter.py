"""No Hands — X/Twitter Platform Module"""
import asyncio

class TwitterPoster:
    def __init__(self, nh): self.nh = nh

    async def post(self, text, video_path=None):
        nh = self.nh
        await nh.goto("https://x.com/compose/post")
        await asyncio.sleep(5)
        if "login" in nh.page.url: return False

        editor = await nh.smart_find(selector='[data-testid="tweetTextarea_0"]') or \
                 await nh.smart_find(role="textbox")
        if editor and not isinstance(editor, dict):
            await editor.click()
            await nh.page.keyboard.type(text, delay=5)

        if video_path:
            await nh.upload_file(video_path)
            for i in range(30):
                await asyncio.sleep(2)
                btn = await nh.page.query_selector('[data-testid="tweetButton"]')
                if btn and await btn.is_enabled(): break

        btn = await nh.page.query_selector('[data-testid="tweetButton"]')
        if btn:
            for i in range(15):
                try:
                    if await btn.is_enabled():
                        await btn.click()
                        nh._log("Twitter: POSTED!", "success")
                        return True
                except: pass
                await asyncio.sleep(1)
            await btn.click(force=True)
            return True
        return False
