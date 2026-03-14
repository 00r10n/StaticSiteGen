import unittest
from enum import Enum
from blocktype import BlockType, block_to_block_type, markdown_to_blocks


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

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )



if __name__ == "__main__":
    unittest.main()
