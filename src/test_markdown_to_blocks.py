import unittest

from textnode import TextNode, TextType
from main import markdown_to_blocks

class TestMarkdownToBlocks(unittest.TestCase):
    def test_given_case(self):
        text = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""
        output = markdown_to_blocks(text)
        expected_output = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            """* This is the first list item in a list block
* This is a list item
* This is another list item"""
            ]
        self.assertEqual(output, expected_output)

    def test_empty_string(self):
        self.assertEqual(markdown_to_blocks(""), [])

    def test_none_case(self):
        with self.assertRaises(ValueError) as context:
            markdown_to_blocks(None)
        self.assertEqual(str(context.exception), "markdown_to_blocks(markdown) requires that markdown be a string")




