"""Entry image for 26 November 2026, picturing six world stories:
Washington's proposed new tariffs on fourteen trading partners; a
drone attack in Kuwait that killed two Italians; EU splits over a
45-billion-euro loan for Ukraine; Ebola cases in DR Congo passing
twelve thousand; a Cairo tanker explosion killing thirty-one people;
and the Macy's Thanksgiving Day parade delayed by a storm."""

import shutil
import struct
import sys
from pathlib import Path

PNG_HEAD = b"\x89PNG\r\n\x1a\n"
BYTE_LIMIT = 1_048_576
SIDE_LIMIT = 1024
HERE = Path(__file__).resolve().parent
ARTWORK = HERE / "entry.png"
TARGET_DIR = Path("/output")
TARGET = TARGET_DIR / "entry.png"


class ArtworkProblem(Exception):
    """Raised when the bundled picture fails one of the entry checks."""


def read_artwork():
    """Load the bundled picture, refusing to continue if it is absent."""
    if not ARTWORK.is_file():
        raise ArtworkProblem(f"artwork file not found: {ARTWORK}")
    data = ARTWORK.read_bytes()
    if len(data) < 29:
        raise ArtworkProblem("artwork file is too short to hold a PNG header")
    return data


def check_magic(data):
    """Make sure the file really begins with the PNG signature."""
    if data[:8] != PNG_HEAD:
        raise ArtworkProblem("artwork does not start with the PNG signature")


def check_byte_size(data):
    """Enforce the one-megabyte ceiling on the entry file."""
    if len(data) > BYTE_LIMIT:
        raise ArtworkProblem(
            f"artwork is {len(data)} bytes, over the {BYTE_LIMIT} byte limit"
        )


def picture_dimensions(data):
    """Pull width and height out of the IHDR chunk, big-endian."""
    if data[12:16] != b"IHDR":
        raise ArtworkProblem("first PNG chunk is not IHDR")
    width, height = struct.unpack_from(">II", data, 16)
    return width, height


def check_sides(width, height):
    """Both sides must be positive and no larger than the limit."""
    for label, side in (("width", width), ("height", height)):
        if side < 1 or side > SIDE_LIMIT:
            raise ArtworkProblem(
                f"artwork {label} is {side}px, outside 1..{SIDE_LIMIT}px"
            )


def deliver(data):
    """Place a copy of the accepted picture at the scoring location."""
    TARGET_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ARTWORK, TARGET)
    print(f"entry accepted: {TARGET} ({len(data)} bytes)")


def confirm_delivery(expected_bytes):
    """Re-read the delivered copy and confirm it survived intact."""
    if not TARGET.is_file():
        raise ArtworkProblem(f"delivered file missing: {TARGET}")
    delivered = TARGET.read_bytes()
    if len(delivered) != expected_bytes:
        raise ArtworkProblem(
            f"delivered file is {len(delivered)} bytes, "
            f"expected {expected_bytes} bytes"
        )
    if delivered[:8] != PNG_HEAD:
        raise ArtworkProblem("delivered file lost its PNG signature")
    print(f"delivery confirmed: {TARGET} ({len(delivered)} bytes)")


def run():
    data = read_artwork()
    check_magic(data)
    check_byte_size(data)
    width, height = picture_dimensions(data)
    check_sides(width, height)
    print(f"entry.png OK: {width}x{height}px, {len(data)} bytes")
    deliver(data)
    confirm_delivery(len(data))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(run())
    except ArtworkProblem as problem:
        print(f"entry rejected: {problem}", file=sys.stderr)
        sys.exit(1)
