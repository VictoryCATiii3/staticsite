import unittest

from textnode import TextType, TextNode
from main import split_nodes_image, split_nodes_link

class TestSplitNodes(unittest.TestCase):
    def test_split_link_simple(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT)
        expexted_output = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
        ]
        output = split_nodes_link([node])
        self.assertEqual(output, expexted_output)

    def test_split_image_simple(self):
        node = TextNode("Here is an image ![Alt text](https://img.com)", TextType.TEXT)
        expected_output = [
                TextNode("Here is an image ", TextType.TEXT),
                TextNode("Alt text", TextType.IMAGE, "https://img.com")
            ]
        self.assertEqual(split_nodes_image([node]), expected_output)

    def test_no_links_or_images(self):
        node = TextNode("This is plain text with no links or images", TextType.TEXT)
        expected_output = [TextNode("This is plain text with no links or images", TextType.TEXT)]
        self.assertEqual(split_nodes_link([node]), expected_output)
        self.assertEqual(split_nodes_image([node]), expected_output)

    def test_link_at_start(self):
        node = TextNode("[Start Link](https://start.com) is at the beginning.", TextType.TEXT)
        expected_output = [
                TextNode("Start Link", TextType.LINK, "https://start.com"),
                TextNode(" is at the beginning.", TextType.TEXT)
            ]
        self.assertEqual(split_nodes_link([node]), expected_output)

    def test_link_at_end(self):
        node = TextNode("This is a sentence with a [final link](https://end.com)", TextType.TEXT)
        expected_output = [
                TextNode("This is a sentence with a ", TextType.TEXT),
                TextNode("final link", TextType.LINK, "https://end.com")
            ]
        self.assertEqual(split_nodes_link([node]), expected_output)

    def test_consecutive_links(self):
        node = TextNode("[Link1](https://1.com)[Link2](https://2.com)", TextType.TEXT)
        expected_output = [
                TextNode("Link1", TextType.LINK, "https://1.com"),
                TextNode("Link2", TextType.LINK, "https://2.com")
            ]
        self.assertEqual(split_nodes_link([node]), expected_output)

    def test_link_with_punctuation(self):
        node = TextNode("This link ([Boot](https://boot.dev)) is inside parentheses.", TextType.TEXT)
        expected_output = [
                TextNode("This link (", TextType.TEXT),
                TextNode("Boot", TextType.LINK, "https://boot.dev"),
                TextNode(") is inside parentheses.", TextType.TEXT)
            ]
        self.assertEqual(split_nodes_link([node]), expected_output)

    def test_only_image(self):
        node = TextNode("![alt text](https://img.com)", TextType.TEXT)
        expected_output = [TextNode("alt text", TextType.IMAGE, "https://img.com")]
        self.assertEqual(split_nodes_image([node]), expected_output)
        self.assertEqual(split_nodes_link([node]), [node])




