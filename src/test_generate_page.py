import unittest
from generate_page import extract_title


class TestGeneratePage(unittest.TestCase):
    def test_extract_title(self):
        md = """
# Here's my h1 title

## This is markdown with multiple blocks

There are paragraphs in here

- List one
- List two
"""
        title = extract_title(md)
        self.assertEqual(title, "Here's my h1 title")

    def test_extract_title_no_matches(self):
        md = """
This markdown doc has not h1 titles.
## This is an h2 title, but it shouldn't match
End of Document
"""
        with self.assertRaises(Exception):
            extract_title(md)

    def test_extract_title_multiple_matches(self):
        md = """
# h1 title one
# h1 title two
Only one h1 title is permitted. Oops!
"""
        with self.assertRaises(Exception):
            extract_title(md)
