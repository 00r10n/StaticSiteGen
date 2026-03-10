import unittest
from parse_text import split_nodes_delimiter, split_nodes_image, split_nodes_link, extract_markdown_images, extract_markdown_links
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

class TestSplitNodesImageSelf(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

class TestSplitNodesLink(unittest.TestCase):
    def test_single_link(self):
        node = TextNode(
            "Hier ist ein [Link zu Google](https://www.google.com)",
            TextType.TEXT,
        )
        result = split_nodes_link([node])
        expected = [
            TextNode("Hier ist ein ", TextType.TEXT),
            TextNode("Link zu Google", TextType.LINK, "https://www.google.com"),
        ]
        self.assertEqual(result, expected)

    def test_multiple_links(self):
        node = TextNode(
            "[Link 1](https://1.com) und [Link 2](https://2.com)",
            TextType.TEXT,
        )
        result = split_nodes_link([node])
        expected = [
            TextNode("Link 1", TextType.LINK, "https://1.com"),
            TextNode(" und ", TextType.TEXT),
            TextNode("Link 2", TextType.LINK, "https://2.com"),
        ]
        self.assertEqual(result, expected)

    def test_link_at_start_end(self):
        node = TextNode(
            "[Link am Anfang](https://start.com) und Text",
            TextType.TEXT,
        )
        result = split_nodes_link([node])
        expected = [
            TextNode("Link am Anfang", TextType.LINK, "https://start.com"),
            TextNode(" und Text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_no_link(self):
        node = TextNode(
            "Nur normaler Text ohne Links",
            TextType.TEXT,
        )
        result = split_nodes_link([node])
        expected = [
            TextNode("Nur normaler Text ohne Links", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_empty_text(self):
        node = TextNode("", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [TextNode("", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_invalid_markdown(self):
        node = TextNode(
            "[Link ohne URL] und ![Bild ohne URL]",
            TextType.TEXT,
        )
        result = split_nodes_link([node])
        expected = [
            TextNode("[Link ohne URL] und ![Bild ohne URL]", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

class TestSplitNodesImage(unittest.TestCase):
    def test_single_image(self):
        node = TextNode(
            "Hier ist ein Bild ![Alt Text](https://image.com/img.png)",
            TextType.TEXT,
        )
        result = split_nodes_image([node])
        expected = [
            TextNode("Hier ist ein Bild ", TextType.TEXT),
            TextNode("Alt Text", TextType.IMAGE, "https://image.com/img.png"),
        ]
        self.assertEqual(result, expected)

    def test_multiple_images(self):
        node = TextNode(
            "![Bild 1](https://1.png) und ![Bild 2](https://2.png)",
            TextType.TEXT,
        )
        result = split_nodes_image([node])
        expected = [
            TextNode("Bild 1", TextType.IMAGE, "https://1.png"),
            TextNode(" und ", TextType.TEXT),
            TextNode("Bild 2", TextType.IMAGE, "https://2.png"),
        ]
        self.assertEqual(result, expected)

    def test_image_and_link_mixed(self):
        node = TextNode(
            "[Link](https://link.com) und ![Bild](https://bild.com)",
            TextType.TEXT,
        )
        result = split_nodes_image([node])
        expected = [
            TextNode("[Link](https://link.com) und ", TextType.TEXT),
            TextNode("Bild", TextType.IMAGE, "https://bild.com"),
        ]
        self.assertEqual(result, expected)

    def test_no_image(self):
        node = TextNode(
            "Nur normaler Text ohne Bilder",
            TextType.TEXT,
        )
        result = split_nodes_image([node])
        expected = [
            TextNode("Nur normaler Text ohne Bilder", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_empty_text(self):
        node = TextNode("", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [TextNode("", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_invalid_markdown(self):
        node = TextNode(
            "![Bild ohne URL] und [Link ohne URL]",
            TextType.TEXT,
        )
        result = split_nodes_image([node])
        expected = [
            TextNode("![Bild ohne URL] und [Link ohne URL]", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
