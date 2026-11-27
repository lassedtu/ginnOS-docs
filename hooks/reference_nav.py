"""Put the generated reference pages into the navigation.

tools/docs/make_reference.py in ginnOS writes docs/reference/, with a
page for each libc header. The set of headers changes with the code, so
mkdocs.yml has only a "Reference" entry, and this hook fills it.
"""

import html
from pathlib import Path

FIRST = ["README.md", "syscalls.md", "ioctls.md"]


def titled(docs_dir, path):
    """A nav entry with the title of the first heading of the page."""
    for line in (Path(docs_dir) / path).read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return {html.unescape(line[2:].strip()): path}
    return path


def on_config(config):
    reference = Path(config.docs_dir) / "reference"
    if not reference.is_dir():
        return config
    pages = [f"reference/{name}" for name in FIRST if (reference / name).is_file()]
    pages += sorted(f"reference/{p.name}" for p in reference.glob("*.md") if p.name not in FIRST)
    libc = reference / "libc"
    if libc.is_dir():
        headers = sorted(f"reference/libc/{p.name}" for p in libc.glob("*.md") if p.name != "README.md")
        pages.append({"libc": ["reference/libc/README.md", *headers]})
    def name(entry):
        if isinstance(entry, str):
            return titled(config.docs_dir, entry)
        return {key: [name(e) for e in value] for key, value in entry.items()}
    pages = [name(e) for e in pages]
    for i, entry in enumerate(config.nav or []):
        if isinstance(entry, dict) and "Reference" in entry:
            config.nav[i] = {"Reference": pages}
    return config
