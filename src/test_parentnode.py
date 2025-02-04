import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_no_tag(self):
        leaf_node = LeafNode("p", "A node")
        main_node = ParentNode(None, [leaf_node])
        with self.assertRaises(ValueError) as context:
            main_node.to_html()
        self.assertEqual(str(context.exception), "ParentNode must have a tag")

    def test_no_child(self):
        node = ParentNode("p", None)
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "ParentNode must have children")

    def test_one_layer(self):
        node = ParentNode(
            "p",
            [LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text")]
        )
        expected_output = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node.to_html(), expected_output)

    def test_nested(self):
        sub_node = ParentNode(
            "b",
            [LeafNode("i", "Bold italic"),
             LeafNode(None, "Normal bold")]
        )
        node = ParentNode(
            "p",
            [LeafNode(None, "Normal text"),
             sub_node,
             LeafNode(None, "More normal text")]
        )
        expected_output = "<p>Normal text<b><i>Bold italic</i>Normal bold</b>More normal text</p>"
        self.assertEqual(node.to_html(), expected_output)








