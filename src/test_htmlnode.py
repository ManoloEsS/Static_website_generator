import unittest
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node


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

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")

    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, "boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "boot.dev", "alt": "This is an image node"},
        )


if __name__ == "__main__":
    unittest.main()
