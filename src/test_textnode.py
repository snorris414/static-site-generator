import unittest
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("Test Node", TextType.ITALIC, "http://example.com")
        self.assertEqual(
            f"TextNode(Test Node, {TextType.ITALIC.value}, http://example.com",
            repr(node),
        )

    def test_noteq(self):
        node = TextNode("`some code`", TextType.CODE)
        node2 = TextNode("`some code`", TextType.PLAIN_TEXT)
        self.assertNotEqual(node, node2)

    def test_no_url(self):
        node = TextNode("blah", TextType.BOLD)
        self.assertEqual(None, node.url)

    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "https://google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertIsNotNone(html_node.props)
        if html_node.props is not None:
            self.assertIsNotNone(html_node.props["href"])
            self.assertEqual(html_node.props["href"], "https://google.com")

    def test_image(self):
        node = TextNode(
            "This is an image node", TextType.IMAGE, "https://example.com/example.png"
        )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertIsNotNone(html_node.props)
        if html_node.props is not None:
            self.assertIsNotNone(html_node.props["src"])
            self.assertEqual(html_node.props["src"], "https://example.com/example.png")
            self.assertIsNotNone(html_node.props["alt"])
            self.assertEqual(html_node.props["alt"], "This is an image node")

    def test_invalid_type(self):
        node = TextNode("This is an invalid node", TextType.PLAIN_TEXT)
        node.text_type = "InvalidType"
        with self.assertRaises(TypeError):
            html_node = text_node_to_html_node(node)

    if __name__ == "__main__":
        unittest.main()
