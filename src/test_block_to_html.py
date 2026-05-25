import unittest
from block_to_html import markdown_to_html_node


class TestBlockToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_quote(self):
        md = """>This is a multiline quote.
> Quotes for days I tell ya.
>Fear is the little death.
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            """<div><blockquote>This is a multiline quote. Quotes for days I tell ya. Fear is the little death.</blockquote></div>""",
        )

    def test_unordered_list(self):
        md = """- item 1
- item 2
- item 3
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html, "<div><ul><li>item 1</li><li>item 2</li><li>item 3</li></ul></div>"
        )

    def test_ordered_list(self):
        md = """1. first item
2. second item
3. third item
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>first item</li><li>second item</li><li>third item</li></ol></div>",
        )

    def test_heading(self):
        md = "### This is a wonderful heading block"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h3>This is a wonderful heading block</h3></div>")

    def test_heading_inline(self):
        md = "## This is a heading with **bold** and _italic_ within"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h2>This is a heading with <b>bold</b> and <i>italic</i> within</h2></div>",
        )

    def test_quote_inline(self):
        md = """>This is a quote block.
>It has _italic content_ within.
>**Bold content** also appears.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote block. It has <i>italic content</i> within. <b>Bold content</b> also appears.</blockquote></div>",
        )

    def test_paragraph_inline(self):
        md = """This is a basic paragraph.
It has some inline elements like _italic_ content.
Some sentences have multiple elements like **bold** and _italic_.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is a basic paragraph. It has some inline elements like <i>italic</i> content. Some sentences have multiple elements like <b>bold</b> and <i>italic</i>.</p></div>",
        )

    def test_unordered_list_inline(self):
        md = """- This is an unordered list
- List item with **bold** and _italic_
- List item with just **bold**
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is an unordered list</li><li>List item with <b>bold</b> and <i>italic</i></li><li>List item with just <b>bold</b></li></ul></div>",
        )

    def test_ordered_list_inline(self):
        md = """1. This is an ordered list
2. List item with **bold** and _italic_
3. List item with just **bold**
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is an ordered list</li><li>List item with <b>bold</b> and <i>italic</i></li><li>List item with just <b>bold</b></li></ol></div>",
        )
