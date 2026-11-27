#!/bin/sh
# Make the reference in build/doxygen/html from the ginnOS checkout (or
# link) in ./ginnOS. The pages.yml workflow and a local build both use it.
#
# The header of each page comes from the Doxygen that runs, so that it
# agrees with that version. The script adds a link back to the manual
# at the top of the side bar.

set -eu

SITE=$(cd "$(dirname "$0")/.." && pwd)
OUT=$SITE/build/doxygen
export SITE

rm -rf "$OUT"
mkdir -p "$OUT"

doxygen -w html "$OUT/header.html" "$OUT/footer.html" "$OUT/default.css" >/dev/null
python3 - "$OUT/header.html" <<'PY'
import sys
path = sys.argv[1]
text = open(path, encoding="utf-8").read()
anchor = '<div id="titlearea">'
link = ('<a id="ginnos-back" href="$relpath^../">'
        '<svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true">'
        '<path d="M15 18l-6-6 6-6" fill="none" stroke="currentColor" '
        'stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
        'The manual</a>')
if text.count(anchor) != 1:
    sys.exit("header.html: the title area was not found one time")
open(path, "w", encoding="utf-8").write(text.replace(anchor, anchor + link))
PY

cd "$SITE/ginnOS"
doxygen "$SITE/doxygen/Doxyfile"
