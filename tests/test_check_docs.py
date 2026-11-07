"""Regression checks for links that can silently break on GitHub Pages."""

from pathlib import Path
import tempfile
import unittest

from scripts.check_docs import check_docs, missing_site_links


class DocumentationChecksTest(unittest.TestCase):
    def test_reports_missing_page_even_if_draft_source_exists(self):
        with tempfile.TemporaryDirectory() as directory:
            site = Path(directory)
            page = site / "index.html"
            page.write_text('<a href="draft.html">Next lesson</a>')
            (site / "draft.ipynb").write_text('{}')
            errors = missing_site_links(site, [page], "/ai-engineering-lab/")
            self.assertEqual(len(errors), 1)
            self.assertIn("draft.html", errors[0])

    def test_relative_and_site_prefixed_assets_resolve(self):
        with tempfile.TemporaryDirectory() as directory:
            site = Path(directory)
            (site / "lessons").mkdir()
            page = site / "lessons/one.html"
            page.write_text('<a href="../index.html?q=1#intro">Home</a>'
                            '<img src="/ai-engineering-lab/image.png">')
            (site / "index.html").write_text('<h1 id="intro">Home</h1>')
            (site / "image.png").write_bytes(b'image')
            self.assertEqual(missing_site_links(site, [page], "/ai-engineering-lab/"), [])

    def test_external_urls_and_fragment_only_links_are_ignored(self):
        with tempfile.TemporaryDirectory() as directory:
            site = Path(directory)
            page = site / "index.html"
            page.write_text('<a href="https://example.com/missing">External</a>'
                            '<a href="//example.com">External</a><a href="#intro">Jump</a>')
            self.assertEqual(missing_site_links(site, [page], ""), [])

    def test_reports_invalid_published_notebook(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / '_quarto.yml').write_text('project:\n  render: [broken.ipynb]\n')
            (root / 'README.md').write_text('# Example')
            (root / 'broken.ipynb').write_text('{not valid JSON')
            errors = check_docs(root)
            self.assertTrue(any('Invalid notebook' in error for error in errors))


if __name__ == "__main__":
    unittest.main()
