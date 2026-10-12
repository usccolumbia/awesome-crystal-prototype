#!/usr/bin/env python3
"""Format and consistency checks for README.md (no network access).

Checks: every list entry is `* [text](url) - description` or `* [text](url) (citation)`, URLs are http(s) (repeated URLs are reported as notes),
every table-of-contents anchor exists, and the data files referenced by the README exist.
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
text = (ROOT / "README.md").read_text()
errors = []
entry = re.compile(r"^\* \[(?P<name>[^\]]+)\]\((?P<url>[^)\s]+)\)(?P<desc> - \S.*| \(.+\))$")
seen = {}
for n, line in enumerate(text.splitlines(), 1):
    if line.startswith("* "):
        m = entry.match(line)
        if not m:
            errors.append(f"line {n}: entry does not match '* [name](url) - description'"); continue
        url = m["url"]
        if not url.startswith(("http://", "https://")):
            errors.append(f"line {n}: URL must be http(s): {url}")
        if url in seen:   # an item may be cross-listed in two sections; report but do not fail
            print(f"  note: line {n} repeats the URL of line {seen[url]}: {url}")
        seen[url] = n
        if not m["desc"].rstrip().endswith((")", "]", ".")):
            errors.append(f"line {n}: entry should end with a citation, [[paper]] link or period")

def anchor(h):
    return re.sub(r"\s+", "-", re.sub(r"[^\w\s-]", "", h.lower()).strip())

anchors = {anchor(l[3:].strip()) for l in text.splitlines() if l.startswith("## ")}
for n, line in enumerate(text.splitlines(), 1):
    m = re.match(r"^- \[[^\]]+\]\(#([^)]+)\)$", line)
    if m and m[1] not in anchors:
        errors.append(f"line {n}: TOC anchor not found: #{m[1]}")
for ref in re.findall(r"\]\(((?:data|assets)/[^)]+|CONTRIBUTING\.md|LICENSE)\)", text):
    if not (ROOT / ref).exists():
        errors.append(f"missing file referenced in README: {ref}")
print(f"{len(seen)} entries checked, {len(errors)} problem(s)")
for e in errors:
    print(" -", e)
sys.exit(1 if errors else 0)
