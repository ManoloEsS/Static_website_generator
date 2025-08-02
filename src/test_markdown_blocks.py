import unittest
from markdown_blocks import (
    markdown_to_blocks,
    block_to_block_type,
    markdown_to_html_node,
    BlockType,
)


class TestHTMLblock(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown_text = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(markdown_text)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_block_type_heading(self):
        md_block = "# This is a heading"
        block_type = block_to_block_type(md_block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_markdown_to_block_type_code(self):
        md_block = "```\nThis is a code\n```"
        block_type = block_to_block_type(md_block)
        self.assertEqual(block_type, BlockType.CODE)

    def test_markdown_to_block_type_quote(self):
        md_block = "> This is a quote\n> more quote"
        block_type = block_to_block_type(md_block)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_markdown_to_block_type_u_list(self):
        md_block = "- This is a list line\n- line also\n- last line"
        block_type = block_to_block_type(md_block)
        self.assertEqual(block_type, BlockType.ULIST)

    def test_markdown_to_block_type_o_list(self):
        md_block = "1. This is number one\n2. This is number 2\n3. This is number 3"
        block_type = block_to_block_type(md_block)
        self.assertEqual(block_type, BlockType.OLIST)

    def test_markdown_to_block_type_normal_paragraph(self):
        md_block = "This is not a heading"
        block_type = block_to_block_type(md_block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


if __name__ == "__main__":
    unittest.main()
