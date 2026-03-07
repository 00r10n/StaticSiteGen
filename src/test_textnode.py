import unittest

from staticSiteGen.src.textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node,node2)

    def test_neq_url(self):
        node = TextNode("abc", TextType.ITALIC, "lalala")
        node2 = TextNode("abc", TextType.ITALIC, "lalal")
        self.assertNotEqual(node,node2)

    def test_neq_text(self):
        node = TextNode("a", TextType.PLAIN)
        node2 = TextNode("b", TextType.PLAIN)
        self.assertNotEqual(node, node2)

    def test_neq_text_type(self):
        node = TextNode("a", TextType.BOLD)
        node2 = TextNode("a", TextType.ITALIC)


if __name__ == "__main__":
    unittest.main()
