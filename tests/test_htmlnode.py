import unittest
from src.htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode()
        node2 = HTMLNode()
        self.assertEqual(node, node2)

    def test_repr(self):
        node = HTMLNode("a", "b", ["a", "b"], {"href": "a", "hello": "b"})
        self.assertEqual(
            repr(node),
            "HTML node=(tag:a, value:b, children:['a', 'b'], props:{'href': 'a', 'hello': 'b'})",
        )

    def test_to_html(self):
        node = HTMLNode(props={"href": "a", "hello": "b"})
        to_html = node.props_to_html()
        self.assertEqual(to_html, ' href="a" hello="b"')

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

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parent_repr(self):
        parentNode = ParentNode("span", ["child_node"], {"href": "a", "hello": "b"})
        self.assertEqual(
            repr(parentNode),
            "ParentNode:(tag:span, children:['child_node'], props:{'href': 'a', 'hello': 'b'})",
        )

    def test_multiple_children(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        child_node2 = ParentNode("span2", [grandchild_node])
        parent_node = ParentNode("div", [child_node, child_node2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span><span2><b>grandchild</b></span2></div>",
        )

    def test_multiple_children_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        child_node2 = ParentNode("span2", [grandchild_node])
        parent_node = ParentNode("div", [child_node, child_node2, grandchild_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span><span2><b>grandchild</b></span2><b>grandchild</b></div>",
        )


if __name__ == "__main__":
    unittest.main()
