import unittest
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
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

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](boot.dev)"
        )
        self.assertListEqual([("to boot dev", "boot.dev")], matches)

    def test_extract_markdown_multiple_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) This is text with an ![image2](//i.imgur.com/zjjcJKZhello.png)"
        )
        self.assertListEqual(
            [
                ("image", "https://i.imgur.com/zjjcJKZ.png"),
                ("image2", "//i.imgur.com/zjjcJKZhello.png"),
            ],
            matches,
        )

    def test_extract_markdown_multiple_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](boot.dev) This is text with a link [to boot.dev](bootdev)"
        )
        self.assertListEqual(
            [("to boot dev", "boot.dev"), ("to boot.dev", "bootdev")], matches
        )

    def test_extract_markdown_links_with_images(self):
        matches = extract_markdown_links("[link](url) and ![alt](img.png)")
        self.assertListEqual([("link", "url")], matches)

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

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](boot.dev) and another [link2](booty.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("link2", TextType.LINK, "booty.dev"),
            ],
            new_nodes,
        )

    def test_split_links_starting_whitespace(self):
        node = TextNode(
            "     This is text with a [link](boot.dev) and another [link2](booty.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("     This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("link2", TextType.LINK, "booty.dev"),
            ],
            new_nodes,
        )

    def test_split_links_ending_whitespace(self):
        node = TextNode(
            "This is text with a [link](boot.dev) and another [link2](booty.dev)      ",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("link2", TextType.LINK, "booty.dev"),
            ],
            new_nodes,
        )

    def test_split_links_no_middle_text(self):
        node = TextNode(
            "This is text with a [link](boot.dev)[link2](booty.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "boot.dev"),
                TextNode("link2", TextType.LINK, "booty.dev"),
            ],
            new_nodes,
        )

    def test_split_links_whitspace_middle(self):
        node = TextNode(
            "This is text with a [link](boot.dev) [link2](booty.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "boot.dev"),
                TextNode("link2", TextType.LINK, "booty.dev"),
            ],
            new_nodes,
        )

    def test_split_links_starting_whitespace_link(self):
        node = TextNode(
            "     [link](boot.dev) and another [link2](booty.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("link2", TextType.LINK, "booty.dev"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )


if __name__ == "__main__":
    unittest.main()
