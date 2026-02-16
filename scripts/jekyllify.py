#!/usr/bin/env python3
"""
Convert legacy static HTML pages to Jekyll pages using the shared layout/includes.

Strategy:
- Skip files that already have YAML front matter.
- Extract <title>, og:title, og:description when present.
- Keep content starting at the first <div class="main">.
- Strip everything from the first <div class="footer"> onwards.

This is intentionally simple and tailored to this repository's structure.
"""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


TITLE_RE = re.compile(r"<title>(.*?)</title>", re.IGNORECASE | re.DOTALL)
OG_TITLE_RE = re.compile(r'<meta\s+property="og:title"\s+content="(.*?)"\s*/?>', re.IGNORECASE)
OG_DESC_RE = re.compile(r'<meta\s+property="og:description"\s+content="(.*?)"\s*/?>', re.IGNORECASE | re.DOTALL)
MYFUNCTION_SCRIPT_RE = re.compile(
    r"<script>\s*function\s+myFunction\s*\(\s*\)\s*\{[\s\S]*?\}\s*</script>\s*",
    re.IGNORECASE,
)


def _cleanup_content(text: str) -> str:
    # Remove the duplicated responsive-nav script (now in assets/js/navmenu.js)
    text = MYFUNCTION_SCRIPT_RE.sub("", text)
    return text


def _first_match(pattern: re.Pattern[str], text: str) -> str | None:
    m = pattern.search(text)
    return None if not m else m.group(1).strip()


def _has_front_matter(text: str) -> bool:
    return text.lstrip().startswith("---\n")


def _yaml_double_quote(value: str) -> str:
    # Escape for a YAML double-quoted scalar
    return value.replace("\\", "\\\\").replace('"', '\\"')


def _split_front_matter(text: str) -> tuple[str, str] | None:
    """Return (front_matter_including_delimiters, rest) or None if absent."""
    stripped = text.lstrip()
    if not stripped.startswith("---\n"):
        return None

    # We only support front matter at the start of the file (no leading spaces).
    if not text.startswith("---\n"):
        return None

    end = text.find("\n---\n", 4)
    if end == -1:
        return None

    end += len("\n---\n")
    return text[:end], text[end:]


def convert_file(path: Path) -> bool:
    raw = path.read_text(encoding="utf-8", errors="replace")
    if _has_front_matter(raw):
        split = _split_front_matter(raw)
        if not split:
            cleaned = _cleanup_content(raw)
            if cleaned != raw:
                path.write_text(cleaned, encoding="utf-8")
                return True
            return False

        fm, rest = split
        main_idx = rest.find('<div class="main">')
        if main_idx != -1:
            rest = rest[main_idx:]

        footer_idx = rest.find('<div class="footer">')
        if footer_idx != -1:
            rest = rest[:footer_idx]

        cleaned = fm + "\n" + _cleanup_content(rest).lstrip()
        if cleaned != raw:
            path.write_text(cleaned, encoding="utf-8")
            return True
        return False

    lang = "en" if path.parts[-2] == "en" else "pt" if path.parts[-2] == "pt" else "pt"

    title = _first_match(TITLE_RE, raw) or "Karate Braga"
    og_title = _first_match(OG_TITLE_RE, raw) or title
    og_desc = _first_match(OG_DESC_RE, raw)
    if og_desc:
        og_desc = " ".join(og_desc.split())

    main_idx = raw.find('<div class="main">')
    if main_idx == -1:
        # If a page doesn't follow the standard structure, leave it unchanged.
        return False

    content = raw[main_idx:]

    footer_idx = content.find('<div class="footer">')
    if footer_idx != -1:
        content = content[:footer_idx]

    content = _cleanup_content(content).rstrip() + "\n"

    fm_lines = [
        "---",
        "layout: default",
        f"lang: {lang}",
        f'title: "{_yaml_double_quote(title)}"',
        f'og_title: "{_yaml_double_quote(og_title)}"',
    ]
    if og_desc:
        fm_lines.append(f'og_description: "{_yaml_double_quote(og_desc)}"')
    fm_lines.append("---")

    new_text = "\n".join(fm_lines) + "\n\n" + content
    path.write_text(new_text, encoding="utf-8")
    return True


def main() -> None:
    html_files = list(ROOT.glob("pt/*.html")) + list(ROOT.glob("en/*.html"))
    changed = 0
    for f in sorted(html_files):
        if convert_file(f):
            changed += 1
    print(f"Converted {changed} files.")


if __name__ == "__main__":
    main()

