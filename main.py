"""make.fun entry: Roast Your Own Operator in One Line.

This script is the entry for the make.fun bounty
"Roast Your Own Operator in One Line"
(https://make.fun/bounty/u-uruteric-roast-your-own-operator-in-one-line-b6485cf1).

It reads the one-line entry from ``line.txt`` (in the same folder as this
script), validates that it is exactly one non-empty line of at most
140 characters, and writes those exact bytes to the output path
(``/output/entry.txt`` by default, or ``$MAKEFUN_OUTPUT`` when set).

No network access. Deterministic: the same input always produces the
same output bytes.
"""

import hashlib
import os
import sys
from pathlib import Path

MAX_CHARS = 140
DEFAULT_OUTPUT = "/output/entry.txt"


def main() -> int:
    source_path = Path(__file__).resolve().parent / "line.txt"
    if not source_path.is_file():
        print(f"error: source file not found: {source_path}", file=sys.stderr)
        return 1
    raw = source_path.read_bytes()

    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        print("error: line.txt is not valid UTF-8", file=sys.stderr)
        return 1

    line = text.rstrip("\r\n")
    if not line:
        print("error: line.txt is empty", file=sys.stderr)
        return 1
    if "\n" in line or "\r" in line:
        print("error: line.txt must contain exactly one line", file=sys.stderr)
        return 1
    if len(line) > MAX_CHARS:
        print(
            f"error: line.txt has {len(line)} characters, "
            f"over the {MAX_CHARS}-character limit",
            file=sys.stderr,
        )
        return 1

    output_path = os.environ.get("MAKEFUN_OUTPUT") or DEFAULT_OUTPUT
    output = Path(output_path)
    if output.parent != Path(""):
        output.parent.mkdir(parents=True, exist_ok=True)

    output.write_bytes(raw)

    expected = hashlib.sha256(raw).hexdigest()
    actual = hashlib.sha256(output.read_bytes()).hexdigest()
    if actual != expected:
        print(
            f"error: output verification failed: SHA-256 mismatch "
            f"(expected {expected}, got {actual})",
            file=sys.stderr,
        )
        return 1

    print(f"wrote {len(raw)} bytes to {output} (sha256 {expected})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
