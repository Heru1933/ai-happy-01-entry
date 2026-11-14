"""ai-happy-01 entry: write our picture to /output/entry.png.

The picture (entry.png beside this file) shows a small fluffy friend
tying a warm red scarf around a happy puppy's neck at sunrise: one
specific, kind moment, drawn to lift the judge's mood at a glance.

The program only copies those bytes, so both grading runs produce the
identical file. Outside the grader's container, MAKEFUN_OUTPUT_DIR
stands in for /output.
"""

import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"
MAX_BYTES = 1_048_576


def output_path() -> Path:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir / "entry.png"


def check_image(data: bytes) -> None:
    """Gate sanity: size cap, and a JPEG or PNG magic header."""
    if len(data) > MAX_BYTES:
        raise SystemExit(f"entry.png is {len(data)} bytes, over the 1 MiB gate")
    if not (data.startswith(b"\xff\xd8\xff") or data.startswith(b"\x89PNG")):
        raise SystemExit("entry.png is neither a JPEG nor a PNG")


def main() -> int:
    data = SOURCE.read_bytes()
    check_image(data)
    target = output_path()
    tmp = target.with_suffix(".tmp")
    tmp.write_bytes(data)
    tmp.replace(target)
    if target.read_bytes() != data:
        raise SystemExit("copied bytes differ from entry.png")
    return 0


if __name__ == "__main__":
    sys.exit(main())
