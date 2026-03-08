import unittest
from parse_text import split_nodes_delimiter
from textnode import TextType, TextNode

class TestParseText(unittest.TestCase):
    def test_codeblock(self):
        node = TextNode("text mit `codeblock`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("text mit ", TextType.TEXT),
                TextNode("codeblock", TextType.CODE)
             ]
        )

    def test_italic(self):
            node = TextNode("text mit _italic_", TextType.TEXT)
            new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
            self.assertEqual(
                new_nodes,
                [
                    TextNode("text mit ", TextType.TEXT),
                    TextNode("italic", TextType.ITALIC)
                ]
            )

    def test_bold(self):
            node = TextNode("text mit **bold**", TextType.TEXT)
            new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
            self.assertEqual(
                new_nodes,
                [
                    TextNode("text mit ", TextType.TEXT),
                    TextNode("bold", TextType.BOLD)
                ]
            )

    def test_with_trail(self):
            node = TextNode("text mit **bold** and rest", TextType.TEXT)
            new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
            self.assertEqual(
                new_nodes,
                [
                    TextNode("text mit ", TextType.TEXT),
                    TextNode("bold", TextType.BOLD),
                    TextNode(" and rest", TextType.TEXT)
                ]
            )

    def test_with_multiple_sects(self):
            node = TextNode("text mit **bold** and rest **and more bold**", TextType.TEXT)
            new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
            self.assertEqual(
                new_nodes,
                [
                    TextNode("text mit ", TextType.TEXT),
                    TextNode("bold", TextType.BOLD),
                    TextNode(" and rest ", TextType.TEXT),
                    TextNode("and more bold", TextType.BOLD)
                ]
            )

    def test_with_neighbours(self):
            node = TextNode("text mit **bold**** and more bold**", TextType.TEXT)
            new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
            self.assertEqual(
                new_nodes,
                [
                    TextNode("text mit ", TextType.TEXT),
                    TextNode("bold", TextType.BOLD),
                    TextNode(" and more bold", TextType.BOLD)
                ]
            )





