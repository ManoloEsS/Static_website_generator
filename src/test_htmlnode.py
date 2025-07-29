import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    # def test_eq(self):
    #     node = HTMLNode()
    #     node2 = HTMLNode()
    #     self.assertEqual(node, node2)
    #
    # def test_repr(self):
    #     node = HTMLNode("a", "b", ["a", "b"], {"href": "a", "hello": "b"})
    #     self.assertEqual(
    #         repr(node),
    #         "HTML node=(tag:a, value:b, children:['a', 'b'], props:{'href': 'a', 'hello': 'b'})",
    #     )
    #
    # def test_to_html(self):
    #     node = HTMLNode(props={"href": "a", "hello": "b"})
    #     to_html = node.props_to_html()
    #     self.assertNotEqual(to_html, ' href="a" hello="b"')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_repr(self):
        node = LeafNode("a", "b", {"href": "a", "hello": "b"})
        self.assertEqual(
            repr(node),
            "LeafNode:(tag:a, value:b, props:{'href': 'a', 'hello': 'b'})",
        )

    def test_leaf_with_props(self):
        node = LeafNode("a", "b", {"href": "a", "hello": "b"})
        self.assertEqual(node.to_html(), '<a href="a" hello="b">b</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")


if __name__ == "__main__":
    unittest.main()
