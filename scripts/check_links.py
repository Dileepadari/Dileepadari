#!/usr/bin/env python3
"""
Checks every link and image in README.md still resolves.

This file renders on a GitHub profile page, so a dead URL is a broken image or
a dead button in front of everyone who visits. That is not hypothetical: the
profile-view counter this README used (`profile-counter.deno.dev`) went away
entirely, and the profile showed a broken-image icon under "Profile Views"
until someone happened to look.

    python scripts/check_links.py

Exits non-zero and lists the failures.

@module checks
"""

import concurrent.futures
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

README = Path(__file__).resolve().parent.parent / "README.md"

# Hosts that answer a scripted request with a refusal rather than the truth.
# Browsing each of these by hand on 2026-09-23 showed a live, correct profile:
# codeforces.com/profile/adaridileep, leetcode.com/u/Delhiking and
# linkedin.com/in/a-dk all resolved. They are skipped rather than deleted so
# this stays a list of known exceptions instead of a silently shorter check.
ANTI_BOT_HOSTS = {
    "codeforces.com": "403 to any non-browser request",
    "leetcode.com": "403 to any non-browser request",
    "www.linkedin.com": "999, LinkedIn's standard scripted-request refusal",
}

USER_AGENT = "Mozilla/5.0 (compatible; profile-readme-link-check)"
TIMEOUT = 30


def urls():
    """Every http(s) URL in an href or src, deduplicated."""
    text = README.read_text(encoding="utf-8")
    return sorted(set(re.findall(r'(?:href|src)="(https?://[^"]+)"', text)))


def host_of(url):
    return url.split("/")[2] if "//" in url else ""


def check(url):
    """Returns (url, None) when fine, or (url, reason) when not."""
    skip = ANTI_BOT_HOSTS.get(host_of(url))
    if skip:
        return url, None
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            if response.status >= 400:
                return url, f"HTTP {response.status}"
            return url, None
    except urllib.error.HTTPError as error:
        return url, f"HTTP {error.code}"
    except Exception as error:  # DNS failure, TLS failure, timeout
        return url, f"{type(error).__name__}: {error}"


def main():
    found = urls()
    if not found:
        # A check that finds nothing to check is not a passing check.
        print("No URLs found in README.md, which cannot be right.", file=sys.stderr)
        return 1

    skipped = [u for u in found if host_of(u) in ANTI_BOT_HOSTS]
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(check, found))

    failures = [(u, why) for u, why in results if why]
    print(f"checked {len(found) - len(skipped)} URLs, skipped {len(skipped)} anti-bot hosts")
    for url in skipped:
        print(f"  skipped {url}  ({ANTI_BOT_HOSTS[host_of(url)]})")
    if failures:
        print(f"\n{len(failures)} dead:", file=sys.stderr)
        for url, why in failures:
            print(f"  {why}  {url}", file=sys.stderr)
        return 1
    print("all good")
    return 0


if __name__ == "__main__":
    sys.exit(main())
