import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode("p", "text einfügen", [1,2,3,4], {"href":"https://www.google.com", "target": "_blank"})
        print(node)
    def test_props_to_html(self):
        node = HTMLNode("p", "text einfügen", [1,2,3,4], {"href":"https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

