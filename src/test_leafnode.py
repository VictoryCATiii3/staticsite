import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_simple_to_html(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")

    def test_url_to_html(self):
        node = LeafNode("a", "Click me!", {"href":"https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_value_error(self):
        with self.assertRaises(ValueError):
            node = LeafNode("p", None)
            node.to_html()

    def test_no_tag(self):
        node = LeafNode(None, "Simple text")
        self.assertEqual(node.to_html(), "Simple text")
