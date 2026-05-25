import unittest
from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_init(self):
        child = LeafNode(None, "child node")
        node = ParentNode("b", [child])
        self.assertEqual(node.tag, "b")
        self.assertEqual(node.children, [child])
        self.assertEqual(node.value, None)
        self.assertEqual(node.props, None)

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_no_tag(self):
        child_node = LeafNode("span", "child")
        parent = ParentNode(None, [child_node], None)
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_to_html_no_children(self):
        parent = ParentNode("div", None, None)
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_to_html_empty_children(self):
        children = []
        parent = ParentNode("div", children, None)
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_to_html_parent_with_props(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node], {"id": "some-id"})
        self.assertEqual(
            parent_node.to_html(),
            '<div id="some-id"><span><b>grandchild</b></span></div>',
        )
