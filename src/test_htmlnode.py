import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test__repr__(self):
        node = HTMLNode("p", "text einfügen", [1,2,3,4], {"href":"https://www.google.com", "target": "_blank"})
        print(node)

    def test_props_to_html(self):
        node = HTMLNode("p", "text einfügen", [1,2,3,4], {"href":"https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_with_prop(self):
        node = LeafNode("a", "value", {"href":"www.abc.de"})
        self.assertEqual(node.to_html(), '<a href="www.abc.de">value</a>')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), '<div><span>child</span></div>')

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            '<div><span><b>grandchild</b></span></div>',
        )
