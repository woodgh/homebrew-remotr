#!/usr/bin/env python3
"""Update the Remotr Cask from the first stable item in its Sparkle feed."""

from __future__ import annotations

import hashlib
import re
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path


FEED_URL = "https://remotr.app/appcast.xml"
DOWNLOAD_PREFIX = (
    "https://download.ducky.build/p/62810754-7260-44e3-b3e1-3b67d378bb1b/"
)
ROOT = Path(__file__).resolve().parents[1]
CASK_PATH = ROOT / "Casks" / "remotr.rb"


def fetch(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "RemotrHomebrewTap/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def main() -> None:
    feed = ET.fromstring(fetch(FEED_URL))
    item = feed.find("./channel/item")
    if item is None:
        raise RuntimeError("No stable release item found in appcast")

    ns = {"sparkle": "http://www.andymatuschak.org/xml-namespaces/sparkle"}
    version = item.findtext("sparkle:shortVersionString", namespaces=ns)
    enclosure = item.find("enclosure")
    if not version or enclosure is None:
        raise RuntimeError("Appcast item is missing version or enclosure")

    version = version.strip()
    url = enclosure.attrib.get("url", "")
    expected_url = f"{DOWNLOAD_PREFIX}Remotr-v{version}.dmg"
    if url != expected_url:
        raise RuntimeError(f"Unexpected release URL for {version}: {url}")

    checksum = hashlib.sha256(fetch(url)).hexdigest()
    cask = CASK_PATH.read_text()
    cask, version_count = re.subn(
        r'^  version "[^"]+"$', f'  version "{version}"', cask, count=1, flags=re.M
    )
    cask, checksum_count = re.subn(
        r'^  sha256 "[0-9a-f]{64}"$', f'  sha256 "{checksum}"', cask, count=1, flags=re.M
    )
    if version_count != 1 or checksum_count != 1:
        raise RuntimeError("Could not update version and checksum in Cask")

    CASK_PATH.write_text(cask)
    print(f"Updated Remotr Cask to {version} ({checksum})")


if __name__ == "__main__":
    main()
