"""No Hands — YouTube Platform Module"""
import asyncio

class YouTubeUploader:
    def __init__(self, nh): self.nh = nh

    async def upload(self, video_path, title, description, privacy="Public"):
        nh = self.nh
        nh._log("YouTube: Starting upload")
        await nh.goto("https://studio.youtube.com")
        await asyncio.sleep(5)
        for _ in range(3): await nh.dismiss_modals()

        await nh.smart_click("Upload videos") or await nh.smart_click("Create")
        await asyncio.sleep(3)
        await nh.smart_click("Upload videos")
        await asyncio.sleep(3)

        if not await nh.upload_file(video_path):
            return False

        for i in range(30):
            await asyncio.sleep(2)
            tbs = await nh.page.query_selector_all('#textbox')
            if len(tbs) >= 2: break

        tbs = await nh.page.query_selector_all('#textbox')
        if len(tbs) >= 1 and await tbs[0].is_visible():
            await tbs[0].click(force=True)
            await nh.page.keyboard.press("Meta+a")
            await nh.page.keyboard.press("Backspace")
            await nh.page.keyboard.type(title, delay=5)
        if len(tbs) >= 2 and await tbs[1].is_visible():
            await tbs[1].click(force=True)
            await nh.page.keyboard.press("Meta+a")
            await nh.page.keyboard.press("Backspace")
            await nh.page.keyboard.type(description, delay=3)

        await nh.smart_click("No, it", aria_label="Not made for kids")

        for _ in range(3):
            await asyncio.sleep(2)
            btn = await nh.page.query_selector('#next-button')
            if btn and await btn.is_visible(): await btn.click()

        await asyncio.sleep(2)
        await nh.smart_click(privacy)
        await asyncio.sleep(1)

        btn = await nh.page.query_selector('#done-button')
        if btn: await btn.click()

        await asyncio.sleep(10)
        nh._log("YouTube: UPLOADED!", "success")
        return True
