"""Copy the 26 November 2026 world-news infographic to /output/entry.png.

Six stories from Thursday 26 November 2026: US tariffs on 14 trade
partners, a Kuwait drone strike that kills two Italians, an EU split
over a EUR45bn Ukraine loan, Ebola passing 12,000 cases in DR Congo,
a Cairo tanker blast killing 31, and the Macy's parade postponed by a
storm. The PNG is validated, then copied unchanged to /output/entry.png.
"""

import os
import shutil
import struct

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1048576
MAX_DIMENSION = 1024


def validate(path):
    size = os.path.getsize(path)
    if size > MAX_BYTES:
        raise ValueError(
            "entry.png is %d bytes, over the %d byte limit" % (size, MAX_BYTES)
        )
    with open(path, "rb") as f:
        header = f.read(24)
    if len(header) < 24 or header[:8] != PNG_SIGNATURE:
        raise ValueError("entry.png does not start with a PNG signature")
    width, height = struct.unpack(">II", header[16:24])
    if width > MAX_DIMENSION or height > MAX_DIMENSION:
        raise ValueError(
            "entry.png is %dx%d, over the %d pixel limit"
            % (width, height, MAX_DIMENSION)
        )


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    validate(src)
    os.makedirs("/output", exist_ok=True)
    dst = os.path.join("/output", "entry.png")
    shutil.copyfile(src, dst)
    print("Copied", src, "to", dst, "(%d bytes)" % os.path.getsize(dst))


if __name__ == "__main__":
    main()
