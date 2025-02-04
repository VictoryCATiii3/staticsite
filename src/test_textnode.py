import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url(self):
        node = TextNode("This is another text node", TextType.ITALIC)
        node2 = TextNode("This is another text node", TextType.ITALIC, None)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("These should be different", TextType.TEXT, "A_URL")
        node2 = TextNode("These should be different", TextType.IMAGE, "A_URL")
        self.assertNotEqual(node, node2)

    def test_url_eq(self):
        node = TextNode("Some text here", TextType.CODE, "Same_URL")
        node2 = TextNode("Some text here", TextType.CODE, "Same_URL")
        self.assertEqual(node, node2)

if __name__=="__main__":
    unittest.main()
