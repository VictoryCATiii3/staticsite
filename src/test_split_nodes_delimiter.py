import unittest

from main import split_nodes_delimiter
from textnode import TextType, TextNode

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code_case(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_output = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected_output)

    def test_early_delim(self):
        node = TextNode("*This block* comes at the beginning", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.BOLD)
        expected_output = [
            TextNode("This block", TextType.BOLD),
            TextNode(" comes at the beginning", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected_output)

    def test_double_delimiter(self):
        node = TextNode("This has **two** bold **words**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_output = [
            TextNode("This has ", TextType.TEXT),
            TextNode("two", TextType.BOLD),
            TextNode(" bold ", TextType.TEXT),
            TextNode("words", TextType.BOLD)
        ]
        self.assertEqual(new_nodes, expected_output)

    def test_single_astrisk(self):
        node = TextNode("This has *only one astrisk", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(str(context.exception), "Invalid markdown syntax")

    def test_multiple_nodes(self):
        node1 = TextNode("This has *two astrisks*", TextType.TEXT)
        node2 = TextNode("This*has two* as well", TextType.BOLD)
        node3 = TextNode("This has *only one astrisk", TextType.CODE)
        node4 = TextNode("This has no astrisks", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1, node2, node3, node4], "*", TextType.BOLD)
        expected_output = [
            TextNode("This has ", TextType.TEXT),
            TextNode("two astrisks", TextType.BOLD),
            TextNode("This*has two* as well", TextType.BOLD),
            TextNode("This has *only one astrisk", TextType.CODE),
            TextNode("This has no astrisks", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected_output)

    def test_empty_list(self):
        nodes = split_nodes_delimiter([], "*", TextType.BOLD)
        self.assertEqual(nodes, [])

    def test_different_delimiters(self):
        node = TextNode("Text with **bold** and `code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_output = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and `code`", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected_output)
        new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
        expected_output = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE)
        ]
        self.assertEqual(new_nodes, expected_output)

