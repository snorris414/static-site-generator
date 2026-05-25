import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_init_no_params(self):
        node = HTMLNode()
        self.assertEqual(None, node.tag)
        self.assertEqual(None, node.value)
        self.assertEqual(None, node.children)
        self.assertEqual(None, node.props)

    def test_to_html(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_props_to_html(self):
        props = {"href": "https://google.com", "target": "_blank"}
        node = HTMLNode("a", "Click here for Google", None, props)
        self.assertEqual(
            ' href="https://google.com" target="_blank"', node.props_to_html()
        )
