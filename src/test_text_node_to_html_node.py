import unittest

from textnode import TextType, TextNode
from leafnode import LeafNode
from main import text_node_to_html_node

class TestTextNodeToHTML(unittest.TestCase):
    def test_text_case(self):
        text_node = TextNode("Simple text", TextType.TEXT)
        node = text_node_to_html_node(text_node)
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, "Simple text")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)
        self.assertEqual(node.to_html(), "Simple text")

    def test_bold_case(self):
        text_node = TextNode("Bold text", TextType.BOLD)
        node = text_node_to_html_node(text_node)
        self.assertEqual(node.tag, "b")
        self.assertEqual(node.value, "Bold text")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)
        self.assertEqual(node.to_html(), "<b>Bold text</b>")

    def test_italic_case(self):
        text_node = TextNode("Italic text", TextType.ITALIC)
        node = text_node_to_html_node(text_node)
        self.assertEqual(node.to_html(), "<i>Italic text</i>")

    def test_code_case(self):
        text_node = TextNode("Code text", TextType.CODE)
        node = text_node_to_html_node(text_node)
        self.assertEqual(node.to_html(), "<code>Code text</code>")

    def test_link_case(self):
        text_node = TextNode("My link", TextType.LINK, "www.google.com")
        node = text_node_to_html_node(text_node)
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "My link")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, {"href":"www.google.com"})
        self.assertEqual(node.to_html(), '<a href="www.google.com">My link</a>')

    def test_image_case(self):
        text_node = TextNode("My cool image", TextType.IMAGE, "www.my_image.com")
        node = text_node_to_html_node(text_node)
        self.assertEqual(node.tag, "img")
        self.assertEqual(node.value, "")
        self.assertEqual(node.props, {"src":"www.my_image.com", "alt":"My cool image"})


