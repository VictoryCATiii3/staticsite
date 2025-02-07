import unittest

from blocks import BlockType, block_to_block_type

class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        self.assertEqual(block_to_block_type("# This is a heading"), BlockType.HEADING)
    def test_code_block(self):
        self.assertEqual(block_to_block_type("```\nprint('hello)\n```"), BlockType.CODE)
    def test_quote_block(self):
        self.assertEqual(block_to_block_type("> This a quote\n> another quote line"), BlockType.QUOTE)
    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("*Item 1\n*Item 2"), BlockType.UNORDERED_LIST)
    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. Item 1\n2. Item 2"), BlockType.ORDERED_LIST)
    def test_paragraph(self):
        text = "This is a normal paragraph"
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

    def test_empty_string(self):
        self.assertEqual(block_to_block_type(""), BlockType.PARAGRAPH)
    def test_mixed_list_style(self):
        text = "* Item 1\n- Item 2"
        self.assertEqual(block_to_block_type(text), BlockType.UNORDERED_LIST)
    def test_invalid_ordered_list(self):
        text = "1. Item 1\n 3. Next item"
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)
    def test_malformed_code_block(self):
        text = "```\nprint('hello world')\n"
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)
