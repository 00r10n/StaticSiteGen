import unittest
from enum import Enum
from blocktype import BlockType, block_to_block_type


class TestBlockToBlockType(unittest.TestCase):

    def test_heading(self):
        block = "# Heading 1"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "## Heading 2"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "###### Heading 6"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_code(self):
        block = "```\nprint('Hello, world!')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote(self):
        block = "> This is a quote\n> With multiple lines"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unordered_list(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        block = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_paragraph(self):
        block = "This is a regular paragraph.\nWith multiple lines."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_edge_cases(self):
        # Empty block
        block = ""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        # Block with only whitespace
        block = "   \n  \n"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        # Block with mixed lines (should not match any special type)
        block = "> This is a quote\n- This is a list item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()
