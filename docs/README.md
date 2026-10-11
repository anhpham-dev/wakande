# Wakande documentation site

This folder is a build-free static site for GitHub Pages.

From the repository root, preview it with:

```sh
python3 -m http.server 8000 --directory docs
```

Open <http://localhost:8000>. The documentation remains readable without JavaScript; JavaScript adds section search, copy buttons, a theme switch, and mobile navigation.

To publish, commit and push this folder, then select **Settings → Pages → Deploy from a branch**, your publishing branch, and **/docs**. See [GitHub's publishing instructions](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).

The default site URL for this repository is <https://anhpham-dev.github.io/wakande/>. All local asset paths are relative so project Pages hosting requires no base-path configuration. `.nojekyll` bypasses Jekyll processing.

## Editing

- `index.html`: documentation content and semantic page structure.
- `assets/styles.css`: responsive layout, colors, typography, and light/dark themes.
- `assets/app.js`: progressive enhancements; no external libraries.
- `assets/favicon.svg`: browser icon.

Keep runnable examples aligned with `lexer.py`, `parser.py`, and `interpreter.py`. Features sketched in `rule.md` and the existing `wak_code/` samples are not all implemented; document them as planned until the interpreter supports them.
