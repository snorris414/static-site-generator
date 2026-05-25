import unittest
from split_blocks import markdown_to_blocks


class TestSplitBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        text = """# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.
Another line to prove the newline.

- This is the first list item in a list block
- This is a list item
- This is another list item


"""

        blocks = markdown_to_blocks(text)
        self.assertEqual(len(blocks), 3)
        self.assertListEqual(
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.\nAnother line to prove the newline.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
            ],
            blocks,
        )

    def test_markdown_to_blocks_2(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
