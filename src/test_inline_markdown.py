import unittest
from inline_markdown import split_nodes_delimiter
from textnode import TextNode, TextType


class TestInLineMarkdown(unittest.TestCase):
    def test_split_nodes_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_split_nodes_multiple_delimiter_code(self):
        node = TextNode(
            "This is text with a `code block` word, and more `code`", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word, and more ", TextType.TEXT),
                TextNode("code", TextType.CODE),
            ],
        )

    def test_split_nodes_no_delimiter_code(self):
        node = TextNode("This is text with a code block word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a code block word", TextType.TEXT),
            ],
        )

    def test_split_nodes_start_delimiter_code(self):
        node = TextNode("`This is text with a code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_split_nodes_end_delimiter_code(self):
        node = TextNode("This is text with a `code block word`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block word", TextType.CODE),
            ],
        )

    def test_split_nodes_unmatched_delimiter_code(self):
        node = TextNode("This is text with a `code block word", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_split_nodes_delimiter_no_text(self):
        node = TextNode("This is text with a code block word", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes, [TextNode("This is text with a code block word", TextType.BOLD)]
        )

    def test_split_nodes_differen_node_types(self):
        nodes = [
            TextNode("Plain text with `code`", TextType.TEXT),
            TextNode("Already bold", TextType.BOLD),
            TextNode("More text with `more code`", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("Plain text with ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode("Already bold", TextType.BOLD),
                TextNode("More text with ", TextType.TEXT),
                TextNode("more code", TextType.CODE),
            ],
        )


if __name__ == "__main__":
    unittest.main()
