from typing import Text
import unittest
from textnode import TextNode, TextType
from splitnodes_delim import (
    extract_markdown_links,
    split_nodes_delimiter,
    extract_markdown_images,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)


class TestSplitNodesDelim(unittest.TestCase):
    def test_split_nodes_code(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN_TEXT)
        old_nodes = [node]
        new_nodes = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.PLAIN_TEXT)

        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)

        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type, TextType.PLAIN_TEXT)

    def test_split_nodes_plain_text(self):
        node = TextNode("This is a basic text node", TextType.PLAIN_TEXT)
        old_nodes = [node]
        new_nodes = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "This is a basic text node")
        self.assertEqual(new_nodes[0].text_type, TextType.PLAIN_TEXT)

    def test_split_nodes_bold(self):
        node = TextNode(
            "This is a node with **several** entries that are **bold**",
            TextType.PLAIN_TEXT,
        )
        old_nodes = [node]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)

        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0].text, "This is a node with ")
        self.assertEqual(new_nodes[0].text_type, TextType.PLAIN_TEXT)
        self.assertEqual(new_nodes[1].text, "several", TextType.BOLD)
        self.assertEqual(new_nodes[2].text, " entries that are ")
        self.assertEqual(new_nodes[2].text_type, TextType.PLAIN_TEXT)
        self.assertEqual(new_nodes[3].text, "bold")
        self.assertEqual(new_nodes[3].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[4].text, "")
        self.assertEqual(new_nodes[4].text_type, TextType.PLAIN_TEXT)

    def test_split_nodes_italic(self):
        node = TextNode("This is an _italic_ node", TextType.PLAIN_TEXT)
        old_nodes = [node]
        new_nodes = split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)

        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is an ")
        self.assertEqual(new_nodes[0].text_type, TextType.PLAIN_TEXT)
        self.assertEqual(new_nodes[1].text, "italic")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[2].text, " node")
        self.assertEqual(new_nodes[2].text_type, TextType.PLAIN_TEXT)

    def test_split_nodes_mix_of_nodes(self):
        node_basic = TextNode("This is a basic text node", TextType.PLAIN_TEXT)
        node_bold = TextNode("This is a **bold** node", TextType.PLAIN_TEXT)
        node_italic = TextNode("This is an _italic_ node", TextType.ITALIC)
        node_code = TextNode("This is a `code` node", TextType.CODE)
        node_bold_2 = TextNode("This second **bold** node", TextType.PLAIN_TEXT)

        old_nodes = [node_basic, node_bold, node_italic, node_code, node_bold_2]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)

        self.assertEqual(len(new_nodes), 9)
        self.assertEqual(new_nodes[0].text, "This is a basic text node")
        self.assertEqual(new_nodes[0].text_type, TextType.PLAIN_TEXT)
        self.assertEqual(new_nodes[1].text, "This is a ")
        self.assertEqual(new_nodes[1].text_type, TextType.PLAIN_TEXT)
        self.assertEqual(new_nodes[2].text, "bold")
        self.assertEqual(new_nodes[2].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[3].text, " node")
        self.assertEqual(new_nodes[3].text_type, TextType.PLAIN_TEXT)
        self.assertEqual(new_nodes[4].text, "This is an _italic_ node", TextType.ITALIC)
        self.assertEqual(new_nodes[4].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[5].text, "This is a `code` node")
        self.assertEqual(new_nodes[5].text_type, TextType.CODE)
        self.assertEqual(new_nodes[6].text, "This second ")
        self.assertEqual(new_nodes[6].text_type, TextType.PLAIN_TEXT)
        self.assertEqual(new_nodes[7].text, "bold")
        self.assertEqual(new_nodes[7].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[8].text, " node")
        self.assertEqual(new_nodes[8].text_type, TextType.PLAIN_TEXT)

    def test_split_nodes_invalid_markdown(self):
        node = TextNode("This is a **node with invalid markdown", TextType.PLAIN_TEXT)
        old_nodes = [node]
        with self.assertRaises(Exception):
            new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)

    def test_split_nodes_no_text_type(self):
        old_nodes = []
        with self.assertRaises(TypeError):
            new_nodes = split_nodes_delimiter(old_nodes, "`", None)

    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        markdown_images = extract_markdown_images(text)
        self.assertIsNotNone(markdown_images)
        self.assertEqual(len(markdown_images), 2)
        self.assertEqual(markdown_images[0][0], "rick roll")
        self.assertEqual(markdown_images[0][1], "https://i.imgur.com/aKaOqIh.gif")
        self.assertEqual(markdown_images[1][0], "obi wan")
        self.assertEqual(markdown_images[1][1], "https://i.imgur.com/fJRm4Vk.jpeg")

    def test_extract_markdown_links_only_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        markdown_links = extract_markdown_links(text)
        self.assertIsNotNone(markdown_links)
        self.assertEqual(len(markdown_links), 0)

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        markdown_links = extract_markdown_links(text)
        self.assertIsNotNone(markdown_links)
        self.assertEqual(len(markdown_links), 2)
        self.assertEqual(markdown_links[0][0], "to boot dev")
        self.assertEqual(markdown_links[0][1], "https://www.boot.dev")
        self.assertEqual(markdown_links[1][0], "to youtube")
        self.assertEqual(markdown_links[1][1], "https://www.youtube.com/@bootdotdev")

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN_TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN_TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_text_at_end(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) and some trailing text",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN_TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN_TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(
                    " and some trailing text",
                    TextType.PLAIN_TEXT,
                ),
            ],
            new_nodes,
        )

    def test_split_images_no_images(self):
        node = TextNode("This is some plain text", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("This is some plain text", TextType.PLAIN_TEXT)], new_nodes
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN_TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN_TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links_text_at_end(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png) and some trailing text",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN_TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN_TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(
                    " and some trailing text",
                    TextType.PLAIN_TEXT,
                ),
            ],
            new_nodes,
        )

    def test_split_links_no_images(self):
        node = TextNode("This is some plain text", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("This is some plain text", TextType.PLAIN_TEXT)], new_nodes
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.PLAIN_TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.PLAIN_TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.PLAIN_TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.PLAIN_TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.PLAIN_TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )
