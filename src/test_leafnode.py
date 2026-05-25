import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_init(self):
        node = LeafNode("b", "some bold text", None)
        self.assertEqual("b", node.tag)
        self.assertEqual("some bold text", node.value)
        self.assertEqual(None, node.props)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_no_value(self):
        node = LeafNode("i", "italic text")
        node.value = None
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "some value")
        self.assertEqual(node.to_html(), node.value)

    def test_leaf_to_html_i(self):
        node = LeafNode("i", "some italic text")
        self.assertEqual(node.to_html(), "<i>some italic text</i>")

    def test_leaf_to_html_a(self):
        props = {"href": "https://neocities.org"}
        node = LeafNode("a", "Visit neocities", props)
        self.assertEqual(
            node.to_html(), '<a href="https://neocities.org">Visit neocities</a>'
        )
