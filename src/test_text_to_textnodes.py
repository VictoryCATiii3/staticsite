import unittest

from textnode import TextNode, TextType
from main import text_to_textnodes

class TestTextToTextNodes(unittest.TestCase):
    def test_given_case(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected_output = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(text_to_textnodes(text), expected_output)

    def test_empty_string(self):
        text = ""
        expected_output = []
        self.assertEqual(text_to_textnodes(text), expected_output)

    def test_input_none(self):
        text = None
        with self.assertRaises(ValueError) as context:
            text_to_textnodes(text)
        self.assertEqual(str(context.exception), "text_to_textnodes(text) requires that text be a string")


