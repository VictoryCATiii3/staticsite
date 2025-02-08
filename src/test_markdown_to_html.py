import unittest

from markdown_to_html import markdown_to_html_node

class TestMarkdownToHtml(unittest.TestCase):
    def test_simple(self):
        text = """
## This is a test

#### Of the markdown_to_html_node function

It has several blocks of text.
This block has multiple lines.
Like 3 lines.

>We also are sticking a quote in here.
>Its a **bold** quote

```
#And we have some code to cause we are sooooo cool
print("hello world")
```

- Unorded list
* Not cool
- mixing tokens
* Why not?

1. Orderd list
2. Very cool
3. Everything matches
"""
        output = markdown_to_html_node(text)
        print("\n--------------------------------------\n")
        print(output.to_html())
        expected_html = '''<div><h2>This is a test</h2><h4>Of the markdown_to_html_node function</h4><p>It has several blocks of text.
This block has multiple lines.
Like 3 lines.</p><blockquote>We also are sticking a quote in here.
Its a <b>bold</b> quote</blockquote><pre><code>
#And we have some code to cause we are sooooo cool
print("hello world")
</code></pre><ul><li>Unorded list</li><li>Not cool</li><li>mixing tokens</li><li>Why not?</li></ul><ol><li>Orderd list</li><li>Very cool</li><li>Everything matches</li></ol></div>'''
        self.assertEqual(output.to_html(), expected_html)

    def test_empty_markdown(self):
        text = ""
        output = markdown_to_html_node(text)
        self.assertEqual(output.to_html(), "<div></div>")

    def test_multiple_newlines(self):
        text = "Paragraph one.\n\n\n\nParagraph two."
        output = markdown_to_html_node(text)
        self.assertEqual(output.to_html(), "<div><p>Paragraph one.</p><p>Paragraph two.</p></div>")

    def test_with_link(self):
        text = "This is a **bold** and *italic* sentence with a [link](https://example.com)."
        output = markdown_to_html_node(text)
        expected_html = '<div><p>This is a <b>bold</b> and <i>italic</i> sentence with a <a href="https://example.com">link</a>.</p></div>'
        self.assertEqual(output.to_html(), expected_html)
