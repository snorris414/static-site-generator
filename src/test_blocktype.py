import unittest
from blocktype import BlockType, block_to_block_type


class TestBlockType(unittest.TestCase):
    def test_heading(self):
        text = "# This is a heading block"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_heading_2(self):
        text = "### This is a heading block"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_heading_no_space(self):
        text = "####This is a heading without the proper space"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_code(self):
        text = """```
This is a valid code block
```"""
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.CODE)

    def test_code_2(self):
        text = """```
This is also a valid code block.
It has multiple lines.
The backticks don't end on their own line```"""
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.CODE)

    def test_code_no_newline(self):
        text = """```This is invalid as it doesn't begin with a newline```"""
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_quote(self):
        text = """>This is a quote block
> There can be a space after the arrow
>The space is completely optional though.
"""
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_quote_missing_arrow(self):
        text = """>This is almost a quote block.
However, it's missing an arrow on this line.
> Therefore, it will end up being a paragraph.
"""

        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_unordered_list_pattern(self):
        text = """- item here
- item there
- item everywhere"""
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_unordered_list_missing_dash(self):
        text = """item here
- item there
- item everywhere"""
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_ordered_list(self):
        text = """1. List item one
2. List item two
3. List item three
4. List item four"""
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_ordered_list_missing_number(self):
        text = """1. List item one
List item without a number
2. List item two
3. List item three"""
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_ordered_list_not_start_with_one(self):
        text = """2. Item two
3. Item three
4. Item four"""
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_ordered_list_non_increasing(self):
        text = """1. Item four
0. Item three
4. Item four"""
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_mixing_list_blocks(self):
        text = """1. Item one
- unordered item
2. item two
- another unordered item
3. item three"""
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_basic_paragraph(self):
        text = """This is a basic paragraph
It has newlines and words galore.
You can imagine so much content."""
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
