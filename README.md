# No Hands 🙌

**The Playwright framework that actually works.**

Built from 100+ real-world automation battles against TikTok, YouTube, Instagram, X, Facebook, iCloud, Suno, and more. Handles every edge case that makes web automation painful.

## The Problem

Playwright is powerful. But every real automation hits the same walls:
- Modals and cookie banners blocking every click
- Shadow DOM components that selectors can't reach
- Anti-bot detection killing headless browsers
- 2FA flows that need human intervention
- File upload dialogs that don't respond to `set_input_files`
- React/SPA apps where elements aren't in the DOM
- Elements behind overlays that can't be clicked
- Multi-step wizards that lose state

You spend 80% of your time fighting the framework instead of building your automation.

## The Solution

```python
from nohands import NoHands

async with NoHands() as nh:
    # Connect to your real Chrome (with all your logins)
    await nh.goto("https://tiktok.com/tiktokstudio/upload")

    # Smart click — tries 10+ strategies, dismisses modals automatically
    await nh.smart_click("Upload videos")

    # Upload with fallbacks (input, file chooser, iframe search)
    await nh.upload_file("/path/to/video.mp4")

    # Fill with retry (placeholder, aria, id, name, JS setter fallback)
    await nh.smart_fill("caption", "My awesome video #viral")

    # Handle 2FA — notifies you via Telegram, waits patiently
    await nh.handle_2fa()

    # Deep navigation — click → wait → screenshot → analyze → repeat
    await nh.deep_navigate([
        {"action": "click", "target": "Next"},
        {"action": "click", "target": "Public"},
        {"action": "click", "target": "Post"},
        {"action": "wait_for_text", "target": "posted successfully"},
    ])
```

## Features

### 🔍 Smart Element Finding (10+ strategies)
```python
# No Hands tries all of these automatically:
el = await nh.smart_find(
    text="Sign In",           # Text content match
    selector="#login-btn",    # CSS selector
    aria_label="Sign in",     # ARIA attribute
    placeholder="Email",      # Placeholder text
    role="button",            # ARIA role
    near_text="Password",    # Nearby label
)
# Falls back through: exact → partial → case-insensitive →
# aria → placeholder → role → JS walk → iframe search → coordinates
```

### 🚫 Auto-Modal Dismissal
Every `smart_click` and `smart_fill` automatically dismisses:
- Cookie consent banners (10+ patterns)
- "Got it" / "OK" / "Not now" popups
- Notification permission dialogs
- Feature announcements
- Overlay blockers

### 📸 Screenshot-Driven Deep Navigation
```python
await nh.deep_navigate([
    {"action": "click", "target": "Create App"},
    {"action": "click", "target": "Other"},
    {"action": "click", "target": "Next"},
    {"action": "fill", "target": "App name", "value": "My App"},
    {"action": "click", "target": "Create"},
    {"action": "wait_for_text", "target": "App created"},
])
# Screenshots after every step. Goes 10+ levels deep.
```

### 🔐 2FA Handler
```python
# Auto-detects 2FA pages, notifies via Telegram, waits for you
await nh.handle_2fa()

# Or provide the code directly
await nh.handle_2fa(code="123456")
```

### 🌐 Platform Modules
Pre-built recipes for common platforms:

```python
from nohands.platforms import TikTokPoster, YouTubeUploader, TwitterPoster

# TikTok — handles all the modals and privacy quirks
tiktok = TikTokPoster(nh)
await tiktok.post("/path/to/video.mp4", "Caption #hashtag")

# YouTube — multi-step wizard with file upload
youtube = YouTubeUploader(nh)
await youtube.upload("/path/to/video.mp4", "Title", "Description")

# Twitter — handles character limits and video processing waits
twitter = TwitterPoster(nh)
await twitter.post("My tweet!", video_path="/path/to/video.mp4")
```

### 🔌 Chrome CDP Connection
Connect to your existing Chrome with all your logins — no need to handle authentication for every site:

```python
# Launch Chrome with: --remote-debugging-port=9222
async with NoHands(chrome_port=9222) as nh:
    # You're already logged into everything!
    await nh.goto("https://studio.youtube.com")
```

### 🤖 Human-Speed Interactions
Anti-bot evasion built in:
- Randomized typing delays
- Natural click timing
- Human-like pauses between actions
- No headless browser fingerprints (uses real Chrome)

## Installation

```bash
pip install no-hands
playwright install chromium
```

## What We Built With It

In one week, using No Hands, one person automated:
- TikTok posting (upload, caption, hashtags, publish)
- YouTube uploads (main video + Shorts)
- X/Twitter posting (text + video)
- Suno AI music generation (40 songs)
- iCloud Photos download (9,000+ videos)
- ElevenLabs voice cloning
- Facebook developer portal navigation
- GitHub repo creation and token generation

All through real Chrome browsers. No headless. No detection. No hands.

## Philosophy

1. **Try everything** — 10+ strategies per element, automatic fallback
2. **Dismiss everything** — Modals are the enemy, kill them on sight
3. **Screenshot everything** — Visual debugging, never guess what went wrong
4. **Wait like a human** — Random delays, natural timing, real Chrome
5. **Handle 2FA gracefully** — Notify, wait, proceed

## License

MIT

## Built by

[Backbone Logic](https://backbonelogic.com) — The team behind CC Swarm.
