# tetsudoku.github.io

Static website for Tetsudoku, served via GitHub Pages.

## Current scope

- `/` — landing page (English), plus `/<lang>/` for eight more languages
- `/privacy/` — Privacy Policy
- `/terms/` — Terms & Conditions

The landing page uses the Figtree webfont (Google Fonts), a rust accent matching
the app icon, and a light/dark toggle that respects the OS preference by default
and persists a manual override in `localStorage`.

`icon.png` is copied from the app repo
(`tetsudoku-kmp/iosApp/iosApp/Assets.xcassets/AppIcon.appiconset/app-icon-1024.png`).
Re-copy it if the app icon changes.

App Store buttons: official Apple "Download on the App Store" badges, localized per
store locale (`badges/appstore-<lang>-{black,white}.svg`, black on light / white on
dark), linking to `https://apps.apple.com/app/id6762089912` (Apple ID from App
Store Connect). The link is dead until the app is published. "Coming soon" context
lives in the surrounding copy, since Apple provides no coming-soon badge variant.
Badges are Apple's official artwork from `toolbox.marketingtools.apple.com` — do
not modify them (App Store marketing guidelines).

## Multi-language build

The landing pages are **generated**. Nine languages (en, de, es, fr, it, ja, ko,
pt-BR, zh-Hans) are produced from a single template + translation file:

- `translations.json` — all copy and per-language metadata
- `template.html` — page template with `{{placeholders}}`
- `build.py` — generator (standard library only, no dependencies)

Edit the copy/template, then run `python3 build.py` to regenerate `index.html`
(English, at root) and `<lang>/index.html` for the rest. **Do not hand-edit the
generated `index.html` files** — they are overwritten on the next build. Commit the
regenerated pages with the source changes. Deployment stays fully static; GitHub
Pages just serves the generated files. Translations follow the app's official App
Store terminology. Legal pages remain English-only.

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
