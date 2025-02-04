import unittest

from main import extract_markdown_images, extract_markdown_links

class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_image(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        output = extract_markdown_images(text)
        expected_output = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(output, expected_output)

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        output = extract_markdown_links(text)
        expected_output = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(output, expected_output)

    def test_dual_one(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and an image ![rick roll](https://i.imgur.com/aKaOqIh.gif) we should only detect one"
        output = extract_markdown_images(text)
        expected_output = [("rick roll", "https://i.imgur.com/aKaOqIh.gif")]
        self.assertEqual(output, expected_output)

    def test_dual_two(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and an image ![rick roll](https://i.imgur.com/aKaOqIh.gif) we should only detect one"
        output = extract_markdown_links(text)
        expected_output = [("to boot dev", "https://www.boot.dev")]
        self.assertEqual(output, expected_output)



#text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
#print(extract_markdown_images(text))
# [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]



#text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
#print(extract_markdown_links(text))
## [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
