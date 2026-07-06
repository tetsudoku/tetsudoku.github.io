# CLAUDE.md

## What this is

The public marketing website for the Tetsudoku app. Plain static HTML/CSS, no
build step, served by GitHub Pages from `main`. Custom domain `tetsudoku.app`
(apex, via `CNAME`).

**This repo is public.** Commit only public-safe content — no local filesystem
paths, secrets, private-repo internals, or unshipped plans. (GitHub Pages also
serves files at the domain, e.g. `tetsudoku.app/CLAUDE.md`.)

## Deploy

Push to `main`; GitHub Pages rebuilds automatically. No CI, no PR flow — commits
land directly on `main` (this repo's established pattern). There is no local dev
server; open the HTML files directly to preview.

## Structure

- `index.html` — landing page
- `styles.css` — all styling (only `index.html` links it)
- `icon.png` — app icon; reused for hero, favicon, apple-touch-icon, OG image
- `appstore-badge-black.svg` / `appstore-badge-white.svg` — official Apple badges
- `privacy/index.html`, `terms/index.html` — legal pages

## Rules and gotchas

**Use relative paths, not root-absolute.** `href="styles.css"`, `src="icon.png"`,
`href="privacy/index.html"` — not `/styles.css`. Root-absolute paths break
`file://` preview (they resolve against the filesystem root). Link to legal pages
as `privacy/index.html` / `terms/index.html` so clicking works under `file://`
too. Keep `og:url` / `og:image` absolute (`https://tetsudoku.app/...`) — social
crawlers require absolute URLs and only ever run against the deployed site.

**Legal pages are generated elsewhere — do not hand-edit them.** `privacy/index.html`
and `terms/index.html` are built in the app repo (`tetsudoku-kmp`) from Termly
exports and copied here verbatim. Edits here are overwritten on the next
regenerate. Change the source over there, then re-copy.

**Shared assets originate in the app repo.** `icon.png` comes from the app's
`AppIcon.appiconset`; re-copy if the icon changes. The App Store badges are
Apple's official artwork (from `toolbox.marketingtools.apple.com`) — do not
modify them (App Store marketing guidelines).

**Theme.** Light/dark is driven by a `data-theme` attribute on `<html>` (persisted
in `localStorage`, set pre-paint to avoid a flash) with a `prefers-color-scheme`
fallback. The rust accent (`#f48638`) matches the app icon. The App Store badge
swaps black-on-light / white-on-dark via the same logic.

**Keep marketing claims aligned with the app's actual behavior.** Notably: the
free tier includes archived **Easy** puzzles only; Medium/Hard/Expert (daily and
archived) plus custom generation require Tetsudoku Unlimited. Verify entitlement
claims against the app before changing pricing copy.

## Launch-day cleanup

The App Store buttons already link to the real listing (dead until the app is
published). Pre-launch "coming soon" wording lives in the copy, not the badge
(Apple has no coming-soon badge). At launch, remove the "Coming soon" wording in
`index.html` — the hero note and the closing CTA section.
