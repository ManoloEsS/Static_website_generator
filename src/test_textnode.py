import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url_is_none(self):
        node = TextNode("This is a link node", TextType.LINK, "boot.dev")
        self.assertNotEqual(node.url, None)

    def test_nodes_not_equal_type(self):
        node = TextNode("I am node", TextType.LINK, "boot.dev")
        node2 = TextNode("I am node", TextType.CODE, "boot.dev")
        self.assertNotEqual(node, node2)

    def test_nodes_not_equal_text(self):
        node = TextNode("I am", TextType.CODE, "boot.dev")
        node2 = TextNode("I am node", TextType.CODE, "boot.dev")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
