# tetsudoku.github.io

Static website for Tetsudoku, served via GitHub Pages.

## Current scope

- `/privacy/` — Privacy Policy
- `/terms/` — Terms & Conditions
- `/` — landing page placeholder (full landing page to come later)

Plain HTML/CSS, no build step.

## Source of truth

The two legal pages are **generated** in the app repo and copied here verbatim:

- `tetsudoku-kmp/docs/legal/privacy-policy.html` → `privacy/index.html`
- `tetsudoku-kmp/docs/legal/terms-and-conditions.html` → `terms/index.html`

Do not hand-edit them here — they are overwritten on the next build over there
(`python3 docs/legal/build-*.py`). Re-copy after regenerating.

## URLs

- Default: `https://tetsudoku.github.io/`
- Custom domain (once DNS is pointed): `https://tetsudoku.app/`

## Custom domain setup (later)

1. Add a `CNAME` file containing `tetsudoku.app`.
2. Point DNS: apex `A`/`AAAA` records to GitHub Pages IPs (or `ALIAS`/`ANAME`),
   and a `CNAME` for `www` → `tetsudoku.github.io`.
3. In repo Settings → Pages, set the custom domain and enable **Enforce HTTPS**.

Do not add the `CNAME` file until DNS is ready — it makes the default
`github.io` URL redirect to the custom domain before it resolves.
