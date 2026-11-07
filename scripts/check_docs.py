"""Validate published notebooks and local links without running model code."""

import argparse
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

import nbformat
import yaml


class PageLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        for attribute in ("href", "src"):
            if attributes.get(attribute):
                self.links.append(attributes[attribute])


def missing_site_links(site, pages, base_path):
    """Check local page/asset paths; external URLs and fragments are excluded."""
    errors = []
    site = site.resolve()
    base_path = base_path.rstrip("/")
    for page in pages:
        parser = PageLinks()
        parser.feed(page.read_text(encoding="utf-8"))
        for href in parser.links:
            url = urlsplit(href)
            if url.scheme or url.netloc or not url.path:
                continue
            path = unquote(url.path)
            if path.startswith("/"):
                if base_path and (path == base_path or path.startswith(base_path + "/")):
                    path = path[len(base_path):]
                target = site / path.lstrip("/")
            else:
                target = page.parent / path
            target = target.resolve()
            if not target.is_relative_to(site):
                errors.append(f"{page}: link leaves site directory: {href}")
                continue
            if target.is_dir():
                target = target / "index.html"
            if not target.is_file():
                errors.append(f"{page}: missing local target: {href}")
    return errors


def check_docs(root, site=None):
    config = yaml.safe_load((root / "_quarto.yml").read_text(encoding="utf-8"))
    sources = [root / name for name in config["project"]["render"]]
    errors = []
    for source in sources:
        if not source.is_file():
            errors.append(f"Missing render source: {source}")
        elif source.suffix == ".ipynb":
            try:
                notebook = nbformat.read(source, as_version=4)
                nbformat.validate(notebook)
            except Exception as exc:
                errors.append(f"Invalid notebook {source}: {exc}")

    # README links resolve in the repository, rather than in the rendered site.
    readme = root / "README.md"
    for href in re.findall(r"\[[^\]]+\]\(([^)]+)\)", readme.read_text(encoding="utf-8")):
        url = urlsplit(href)
        if not url.scheme and not url.netloc and url.path:
            if not (root / unquote(url.path)).exists():
                errors.append(f"README.md: missing local target: {href}")

    if site is not None:
        pages = [site / source.relative_to(root).with_suffix(".html") for source in sources]
        for page in pages:
            if not page.is_file():
                errors.append(f"Missing rendered page: {page}")
        errors.extend(missing_site_links(
            site, [page for page in pages if page.is_file()],
            urlsplit(config["website"].get("site-url", "")).path,
        ))
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site", type=Path, help="Also check a rendered site directory")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    errors = check_docs(root, args.site.resolve() if args.site else None)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("Documentation checks passed (notebook structure and local link targets).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
