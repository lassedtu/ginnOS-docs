# ginnOS docs site

This repository builds the ginnOS docs site and publishes it at
<https://lassedtu.github.io/ginnOS-docs/>. It has no pages. The pages
are in [`docs/`](https://github.com/lassedtu/ginnOS/tree/main/docs) of
the ginnOS repository, and the rules for them are in
[`docs/WRITING.md`](https://github.com/lassedtu/ginnOS/blob/main/docs/WRITING.md).

| File | What it is |
| --- | --- |
| `mkdocs.yml` | the site: the theme, the Markdown extensions, the navigation |
| `requirements.txt` | the mkdocs and Material versions |
| `theme/stylesheets/ginnos.css` | the ginnOS look: the colours, fonts and radii of idunn (`src/lib/idunn/theme.c`) on top of Material |
| `hooks/cachebust.py` | adds a hash of each stylesheet to its address, so that a browser does not mix old and new stylesheets |
| `doxygen/Doxyfile` | the reference: the Doxygen settings of ginnOS (`tools/docs/Doxyfile`), with the stylesheets below and the output folder |
| `theme/doxygen/` | the look of the reference: [doxygen-awesome-css](https://github.com/jothepro/doxygen-awesome-css) 2.5.0 (MIT, see its `LICENSE`) and `ginnos.css`, which gives it the colours and fonts of the site |
| `.github/workflows/pages.yml` | builds the site and the reference, and publishes them on GitHub Pages |

## See the site on your computer

1. Install mkdocs and the Material theme:

   ```sh
   uv tool install mkdocs --with mkdocs-material
   ```

   Or use `pip install -r requirements.txt`.

2. Make `ginnOS` a link to your checkout of the ginnOS repository. Git
   ignores the link.

   ```sh
   ln -s ../../Projekter/ginnOS ginnOS
   ```

3. Start the server and open <http://127.0.0.1:8000/ginnOS-docs/>:

   ```sh
   mkdocs serve
   ```

   The site changes when you save a page.

4. To see the reference, install Doxygen 1.17 or later, then run:

   ```sh
   SITE=$PWD; (cd ginnOS && SITE=$SITE doxygen $SITE/doxygen/Doxyfile)
   ```

   and open `build/doxygen/html/index.html`. On the published site the
   reference is at `/reference/`.

## How the site gets published

The workflow builds the site when one of these occurs:

- ginnOS sends the `docs-changed` event. Its workflow
  `.github/workflows/docs.yml` does that when a push to `main` changes
  `docs/`, `src/` or `tools/docs/`. The event carries the commit, and the site builds from that
  commit.
- A push to `main` of this repository.
- You start the workflow by hand (Actions, pages, Run workflow). The
  `ref` field selects the ginnOS branch or commit; the default is `main`:

  ```sh
  gh workflow run pages --repo lassedtu/ginnOS-docs -f ref=docs
  ```

When you add or remove a page in ginnOS, change `nav` in `mkdocs.yml`
too. The build uses `strict: true`, so it stops on a broken link or on a
page that is not in `nav`.
