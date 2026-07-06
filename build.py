#!/usr/bin/env python3
"""Generate the per-language landing pages from template.html + translations.json.

Static site generator with no runtime dependency: run this locally whenever the
copy or template changes, then commit the generated HTML. GitHub Pages serves the
output as plain static files.

  English -> /index.html          (site root, lang "en")
  others  -> /<path>/index.html   (e.g. /de/, /ja/, /zh-Hans/)

Each page gets its own <title>, meta description, og: tags, <html lang>, canonical
URL, and a full set of hreflang alternates. The language <select> in the header
links to the sibling page in every language. Run: python3 build.py
"""

import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))

# Placeholders whose values are already HTML/URLs and must NOT be escaped.
RAW_KEYS = {
    "base", "badge", "lang", "canonical", "domain", "og_locale",
    "hreflang_links", "lang_options", "free_features", "unlimited_features",
}


def load():
    with open(os.path.join(ROOT, "translations.json"), encoding="utf-8") as f:
        data = json.load(f)
    with open(os.path.join(ROOT, "template.html"), encoding="utf-8") as f:
        template = f.read()
    return data, template


def page_url(domain, path):
    return domain + "/" + (path + "/" if path else "")


def render(template, values):
    def sub(match):
        key = match.group(1)
        if key not in values:
            raise KeyError(f"template placeholder {{{{{key}}}}} has no value")
        val = values[key]
        return val if key in RAW_KEYS else html.escape(val, quote=True)

    return re.sub(r"\{\{(\w+)\}\}", sub, template)


def main():
    data, template = load()
    domain = data["site"]["domain"]
    brand = data["site"]["brand"]
    languages = data["languages"]
    strings = data["strings"]

    warnings = []
    for lang in languages:
        code = lang["code"]
        if code not in strings:
            warnings.append(f"missing translations for {code}")
            continue
        for variant in ("black", "white"):
            badge = os.path.join(ROOT, "badges", f"appstore-{code}-{variant}.svg")
            if not os.path.exists(badge):
                warnings.append(f"missing badge {badge}")

    pages = 0
    for lang in languages:
        code = lang["code"]
        path = lang["path"]
        s = strings[code]
        base = "" if path == "" else "../"

        # hreflang alternates (absolute URLs) + x-default -> English root
        hreflang = []
        for other in languages:
            hreflang.append(
                f'  <link rel="alternate" hreflang="{other["hreflang"]}" '
                f'href="{page_url(domain, other["path"])}">'
            )
        hreflang.append(
            f'  <link rel="alternate" hreflang="x-default" href="{page_url(domain, "")}">'
        )

        # Language <select> options: relative links that also work under file://
        options = []
        for other in languages:
            target = base + ("index.html" if other["path"] == ""
                             else other["path"] + "/index.html")
            selected = " selected" if other["code"] == code else ""
            options.append(
                f'        <option value="{target}"{selected}>'
                f'{html.escape(other["name"])}</option>'
            )

        def items(key):
            return "\n".join(
                f"            <li>{html.escape(x, quote=True)}</li>" for x in s[key]
            )

        values = {
            "lang": code,
            "base": base,
            "badge": code,
            "domain": domain,
            "og_locale": lang["locale"],
            "canonical": page_url(domain, path),
            "hreflang_links": "\n".join(hreflang),
            "lang_options": "\n".join(options),
            "title": f"{brand}: {s['tagline']}",
            "free_features": items("free_features"),
            "unlimited_features": items("unlimited_features"),
        }
        # Copy the remaining flat string keys through verbatim.
        for k, v in s.items():
            if isinstance(v, str):
                values[k] = v

        out_html = render(template, values)

        out_dir = ROOT if path == "" else os.path.join(ROOT, path)
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, "index.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(out_html)
        pages += 1
        print(f"  {os.path.relpath(out_path, ROOT)}")

    print(f"Generated {pages} pages.")
    if warnings:
        print("\nWARNINGS:")
        for w in warnings:
            print(f"  - {w}")
        sys.exit(1)


if __name__ == "__main__":
    main()
