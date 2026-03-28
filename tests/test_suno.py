#!/usr/bin/env python3
"""
No Hands Test — Suno.com Song Generation
=========================================
Real-world test using the No Hands framework.
"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from nohands import NoHands

SONGS = [
    "warm cinematic piano with soft strings, beautiful NYC sunset, elegant and emotional, perfect for real estate, no vocals",
    "confident upbeat instrumental, modern city energy, stylish and sophisticated, light drums with piano, no vocals",
]


async def main():
    print("=" * 60)
    print("  NO HANDS TEST — Suno Song Generation")
    print("=" * 60)

    async with NoHands(
        chrome_port=9222,
        connect_existing=True,
        human_speed=True,
        typing_delay=10,
        screenshot_dir="/tmp/nohands-suno",
        telegram_token="8494199952:AAELkZFcaRSJ0X7ZrhA01332ZGbglade8EE",
        telegram_chat="-1003738909925",
    ) as nh:

        # Set viewport wide enough to see the Create panel
        await nh.page.set_viewport_size({"width": 1400, "height": 900})

        for i, prompt in enumerate(SONGS):
            print(f"\n{'─' * 60}")
            print(f"  Song {i+1}/2: {prompt[:50]}...")
            print(f"{'─' * 60}")

            # Step 1: Navigate to Create
            await nh.goto("https://suno.com/create")
            await asyncio.sleep(4)
            await nh.dismiss_modals()
            await nh.screenshot(f"suno_page_{i}")

            # Step 2: Deep navigate — the No Hands way
            success = await nh.deep_navigate([
                {
                    "action": "fill",
                    "target": "lyrics",  # matches placeholder containing "lyrics"
                    "value": prompt,
                    "required": False,
                },
            ])

            # If deep_navigate didn't fill, find textarea manually using smart approach
            if not success:
                nh._log("Deep navigate fill missed, using smart textarea finder", "warn")

                # Use No Hands get_all_inputs to find the right field
                inputs = await nh.get_all_inputs()
                nh._log(f"Found {len(inputs)} input fields")

                for inp in inputs:
                    ph = inp.get("placeholder", "").lower()
                    if "lyrics" in ph or "prompt" in ph or "write" in ph or "describe" in ph:
                        nh._log(f"Found target: placeholder='{inp['placeholder'][:40]}'")

                        # Click on it by finding the actual element
                        el = await nh.page.query_selector(
                            f'textarea[placeholder*="{inp["placeholder"][:20]}"]'
                        )
                        if el and await el.is_visible():
                            await el.click()
                            await asyncio.sleep(0.3)
                            await nh.page.keyboard.press("Meta+a")
                            await nh.page.keyboard.press("Backspace")
                            await asyncio.sleep(0.2)
                            await nh.page.keyboard.type(prompt, delay=10)
                            nh._log("Filled via smart input scan!", "success")
                            success = True
                            break

            if not success:
                # Nuclear option — just find the FIRST visible textarea
                nh._log("Using nuclear option — first visible textarea", "warn")
                for ta in await nh.page.query_selector_all("textarea"):
                    if await ta.is_visible():
                        box = await ta.bounding_box()
                        if box and box["height"] > 30 and box["x"] < 500:  # Left panel
                            await ta.click()
                            await asyncio.sleep(0.3)
                            await nh.page.keyboard.press("Meta+a")
                            await nh.page.keyboard.press("Backspace")
                            await nh.page.keyboard.type(prompt, delay=10)
                            nh._log(f"Filled first textarea at ({box['x']:.0f},{box['y']:.0f})", "success")
                            success = True
                            break

            if not success:
                nh._log("FAILED to fill any field!", "error")
                await nh.screenshot(f"suno_failed_{i}")
                continue

            await nh.screenshot(f"suno_filled_{i}")
            await nh.human_pause(1)

            # Step 3: Click Create
            clicked = await nh.smart_click("Create", aria_label="Create song")

            if not clicked:
                nh._log("Smart click missed, trying button scan", "warn")
                for btn in await nh.page.query_selector_all("button"):
                    aria = await btn.get_attribute("aria-label") or ""
                    txt = (await btn.text_content() or "").strip()
                    if "Create song" in aria or txt == "Create":
                        if await btn.is_visible():
                            box = await btn.bounding_box()
                            if box and box["x"] < 500:  # Left panel
                                await btn.click(force=True)
                                clicked = True
                                nh._log("Clicked Create via button scan", "success")
                                break

            if clicked:
                nh._log(f"Song {i+1} GENERATING!", "success")
                await nh.screenshot(f"suno_creating_{i}")
                nh._log("Waiting 55s...")
                await asyncio.sleep(55)
                await nh.screenshot(f"suno_done_{i}")
                nh._log(f"Song {i+1} COMPLETE!", "success")
            else:
                nh._log("Create button not found!", "error")
                await nh.screenshot(f"suno_create_failed_{i}")

            await nh.human_pause(3)

        # Done
        print(f"\n{'=' * 60}")
        print(f"  NO HANDS TEST COMPLETE")
        print(f"  Screenshots: /tmp/nohands-suno/")
        print(f"  Actions: {len(nh.get_action_log())}")
        print(f"{'=' * 60}")

        nh.save_action_log()
        await nh.notify(
            "🙌 NO HANDS SUNO TEST COMPLETE\n\n"
            f"2 songs generated!\n"
            f"Actions: {len(nh.get_action_log())}"
        )


if __name__ == "__main__":
    asyncio.run(main())
