"""Add the hash of each own stylesheet to its URL.

GitHub Pages lets a browser keep a file for ten minutes. Without the hash,
a page from a new build can get the stylesheet of an old build. With the
hash, each page asks for the stylesheet that it was built with.
"""

import hashlib
from pathlib import Path


def on_config(config):
    theme_dir = Path(config.config_file_path).parent / "theme"
    urls = []
    for url in config.extra_css:
        path = theme_dir / str(url)
        if path.is_file():
            digest = hashlib.sha256(path.read_bytes()).hexdigest()[:10]
            url = f"{url}?h={digest}"
        urls.append(url)
    config.extra_css = urls
    return config
