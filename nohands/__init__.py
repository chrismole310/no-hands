"""
No Hands — The Playwright Framework That Actually Works
=======================================================
Built from 100+ real-world automation battles.
Handles modals, 2FA, shadow DOM, anti-bot, file uploads, and everything else.

Usage:
    from nohands import NoHands

    async with NoHands() as nh:
        await nh.goto("https://example.com")
        await nh.smart_click("Sign In")
        await nh.smart_fill("email", "user@example.com")
        await nh.smart_fill("password", "secret")
        await nh.smart_click("Submit")
        await nh.handle_2fa()  # Waits for you, notifies via Telegram
"""

__version__ = "0.1.0"
__author__ = "Backbone Logic / Chris Mole"

from .core import NoHands
from .navigator import DeepNavigator
from .elements import SmartElement
from .auth import TwoFactorHandler
