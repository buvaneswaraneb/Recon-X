# modules/username_search.py — Check username existence across platforms
# Based on 11_username_search.py; extended with HTTP probing and status codes.

import urllib.request
import urllib.error
import threading
import ssl
from core.base import BaseModule
from core.config import C
from utils.helpers import pause

# (Platform, URL template, HTTP status that means "found")
PLATFORMS: list[tuple[str, str, int]] = [
    ("GitHub",         "https://github.com/{}",                200),
    ("GitLab",         "https://gitlab.com/{}",                200),
    ("Instagram",      "https://www.instagram.com/{}/",        200),
    ("Reddit",         "https://www.reddit.com/user/{}/",      200),
    ("Twitch",         "https://www.twitch.tv/{}",             200),
    ("X / Twitter",    "https://x.com/{}",                     200),
    ("YouTube",        "https://www.youtube.com/@{}",          200),
    ("TikTok",         "https://www.tiktok.com/@{}",           200),
    ("Pinterest",      "https://www.pinterest.com/{}/",        200),
    ("Tumblr",         "https://{}.tumblr.com/",               200),
    ("Medium",         "https://medium.com/@{}",               200),
    ("Dev.to",         "https://dev.to/{}",                    200),
    ("Keybase",        "https://keybase.io/{}",                200),
    ("HackerNews",     "https://news.ycombinator.com/user?id={}", 200),
    ("Replit",         "https://replit.com/@{}",               200),
    ("Pastebin",       "https://pastebin.com/u/{}",            200),
    ("Linktree",       "https://linktr.ee/{}",                 200),
    ("Steam",          "https://steamcommunity.com/id/{}",     200),
    ("Twitch (clips)", "https://clips.twitch.tv/{}",           200),
    ("Mastodon",       "https://mastodon.social/@{}",          200),
]

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode    = ssl.CERT_NONE


class UsernameSearch(BaseModule):
    NAME  = "Username Search"
    COLOR = C.RED
    DESC  = "Probe username existence across 20+ platforms"

    def __init__(self):
        self._results: list[tuple[str, str, bool]] = []
        self._lock = threading.Lock()

    def _check(self, username: str, platform: str, url: str, expected: int) -> None:
        final_url = url.format(username)
        req = urllib.request.Request(
            final_url,
            headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"},
        )
        found = False
        try:
            with urllib.request.urlopen(req, context=CTX, timeout=6) as resp:
                found = (resp.status == expected)
        except urllib.error.HTTPError as e:
            found = (e.code == expected)
        except Exception:
            pass

        with self._lock:
            self._results.append((platform, final_url, found))
            if found:
                print(f"  {C.OK}✔ {C.BOLD}{platform:<22}{C.RESET}  {C.DIM}{final_url}{C.RESET}")

    def run(self) -> None:
        self.header()
        username = self.prompt("Enter username", self.COLOR)
        if not username:
            self.err("No username provided."); pause(); return

        self._results.clear()
        self.info(f"Checking '{username}' across {len(PLATFORMS)} platforms …\n")

        threads = []
        for platform, url, expected in PLATFORMS:
            t = threading.Thread(
                target=self._check,
                args=(username, platform, url, expected),
                daemon=True,
            )
            threads.append(t)
            t.start()
        for t in threads:
            t.join()

        found = [r for r in self._results if r[2]]
        not_found = [r for r in self._results if not r[2]]

        print()
        self.ok(f"Found on {len(found)} / {len(PLATFORMS)} platforms.")
        if not_found:
            self.warn(f"Not found / unreachable: {len(not_found)} platform(s).")

        # Optionally list not-found
        show = self.prompt("\nList platforms NOT found? [y/N]", C.DIM).lower()
        if show == "y":
            print()
            for platform, url, _ in sorted(not_found, key=lambda x: x[0]):
                print(f"  {C.DIM}✘ {platform}{C.RESET}")

        pause()
