"""The Funniest Excuse for Skipping a Meeting — make.fun entry (program/v1).

Writes one excuse line (128 characters, UTF-8, no trailing newline) to
/output/entry.txt.

The excuse is not a stock alibi about wifi, a cat, or a dentist: it is
the deja-vu of the recurring meeting itself. The speaker has already sat
through this exact meeting in 2019, in 2021, and last Tuesday, and the
ending never changes — so skipping it is not dodging work, it is refusing
to rewatch a meeting whose outcome is already known. The laugh lands
with a nod of recognition from anyone who has ever watched the same
agenda come back, year after year, with nothing ever decided.

Standard library only. No network, no local imports, no writes
outside the output path the harness provides. Deterministic: the
same bytes on every run.
"""

import os
import sys

ENTRY = (
    "Sorry, I can't make it \u2014 I already sat through this exact "
    "meeting in 2019, 2021, and last Tuesday, and the ending never changes."
)


def main():
    line = ENTRY
    if not line or not line.strip():
        sys.exit("entry line is blank")
    if "\n" in line or "\r" in line:
        sys.exit("entry line must be a single line")
    if not 1 <= len(line) <= 200:
        sys.exit("entry line must be 1-200 characters, got %d" % len(line))
    if line != line.strip():
        sys.exit("entry line must not start or end with whitespace")
    if "  " in line:
        sys.exit("entry line must not contain double spaces")
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in line):
        sys.exit("entry line must not contain control characters")
    if "meeting" not in line.lower():
        # The excuse must stay on the subject: skipping a meeting.
        sys.exit("entry line must be an excuse for skipping a meeting")
    if "2019" not in line or "2021" not in line or "last Tuesday" not in line:
        # The three repeat attendances are the joke: this meeting has
        # already happened, more than once, with the same ending.
        sys.exit("entry line must keep the three repeat attendances")
    if "ending never changes" not in line:
        # The punchline is that the meeting's outcome is already known.
        sys.exit("entry line must keep the ending-never-changes punchline")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = line.encode("utf-8")
    with open(path, "wb") as fh:
        fh.write(data)
    # Re-read and verify the file is exactly the gated line, no newline.
    with open(path, "rb") as fh:
        written = fh.read()
    if written != data:
        sys.exit("entry.txt does not match the gated line")
    print("wrote %s (%d chars, %d bytes)" % (path, len(line), len(data)))


if __name__ == "__main__":
    main()
