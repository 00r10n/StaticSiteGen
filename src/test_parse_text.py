import unittest
from parse_text import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
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


class TestImageParse(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

class TestLinkParse(unittest.TestCase):
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)



class TestMarkdownExtractor(unittest.TestCase):

    def test_extract_markdown_links(self):
        # Test: Einfacher Markdown-Link
        text = "Hier ist ein [Link](https://example.com)."
        result = extract_markdown_links(text)
        self.assertEqual(result, [("Link", "https://example.com")])

        # Test: Mehrere Links
        text = "[Link1](https://example.com) und [Link2](https://test.org)."
        result = extract_markdown_links(text)
        self.assertEqual(result, [
            ("Link1", "https://example.com"),
            ("Link2", "https://test.org")
        ])

        # Test: Keine Links
        text = "Keine Links hier."
        result = extract_markdown_links(text)
        self.assertEqual(result, [])

        # Test: Ungültige Markdown-Syntax
        text = "[Link ohne URL] und [Link2](https://test.org)."
        result = extract_markdown_links(text)
        self.assertEqual(result, [("Link2", "https://test.org")])

        # Test: Leere Strings
        text = ""
        result = extract_markdown_links(text)
        self.assertEqual(result, [])

    def test_extract_markdown_images(self):
        # Test: Einfaches Markdown-Bild
        text = "Hier ist ein Bild: ![Alt Text](https://example.com/image.png)."
        result = extract_markdown_images(text)
        self.assertEqual(result, [("Alt Text", "https://example.com/image.png")])

        # Test: Mehrere Bilder
        text = "![Alt1](https://example.com/1.png) und ![Alt2](https://test.org/2.png)."
        result = extract_markdown_images(text)
        self.assertEqual(result, [
            ("Alt1", "https://example.com/1.png"),
            ("Alt2", "https://test.org/2.png")
        ])

        # Test: Keine Bilder
        text = "Keine Bilder hier."
        result = extract_markdown_images(text)
        self.assertEqual(result, [])

        # Test: Ungültige Markdown-Syntax
        text = "![Alt ohne URL] und ![Alt2](https://test.org/2.png)."
        result = extract_markdown_images(text)
        self.assertEqual(result, [("Alt2", "https://test.org/2.png")])

        # Test: Leere Strings
        text = ""
        result = extract_markdown_images(text)
        self.assertEqual(result, [])

