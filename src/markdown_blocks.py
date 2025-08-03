from enum import Enum
from src.htmlnode import LeafNode, ParentNode
from src.textnode import TextNode, TextType, text_node_to_html_node
from src.inline_markdown import text_to_textnodes


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"


def markdown_to_blocks(markdown_text: str) -> list[str]:
    """Function that splits a markdown file into a list of separated strings
    that will be converted to html blocks"""

    blocks = markdown_text.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks


def block_to_block_type(markdown_block: str) -> BlockType:
    """Function that checks and returns the type of HTML block a markdown block is
    and returns the BlockType"""

    lines = markdown_block.split("\n")

    if markdown_block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    elif len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    elif markdown_block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    elif markdown_block.startswith(("- ", "* ")):
        for line in lines:
            if not line.startswith(("- ", "* ")):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    elif markdown_block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown: str) -> ParentNode:
    """Function that converts a full markdown document into a parent Parentnode with multiple children"""

    markdown_blocks = markdown_to_blocks(markdown)
    children = []
    for block in markdown_blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block: str) -> ParentNode:
    """Helper function that returns an html node based on the block type calling {BlockType}_to_html_node functions"""
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.ULIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.OLIST:
        return olist_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")


def text_to_children(text: str) -> list[LeafNode]:
    """Helper function that takes a string and returns a list of LeafNodes"""

    children_nodes = []
    text_nodes = text_to_textnodes(text)
    for node in text_nodes:
        new_html_node = text_node_to_html_node(node)
        children_nodes.append(new_html_node)
    return children_nodes


def heading_to_html_node(block: str) -> ParentNode:
    """Helper function that creates a ParentNode from a heading markdown block"""

    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block: str) -> ParentNode:
    """Helper function that takes a code block and creates a parent node
    with the 'pre' tag that nests the code html node"""

    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def ulist_to_html_node(block: str) -> ParentNode:
    """Helper function that returns a unordered list Parent node from a text block"""

    split_block = block.split("\n")
    html_items = []
    for item in split_block:
        text = item[2:]
        html_children = text_to_children(text)
        html_items.append(ParentNode("li", html_children))
    return ParentNode("ul", html_items)


def olist_to_html_node(block: str) -> ParentNode:
    """Helper function that returns an ordered list parent node from a text block"""

    split_block = block.split("\n")
    html_items = []
    for item in split_block:
        text = item[3:]
        html_children = text_to_children(text)
        html_items.append(ParentNode("li", html_children))
    return ParentNode("ol", html_items)


def quote_to_html_node(block: str) -> ParentNode:
    """Helper function that returns a quote parent node from a text block"""

    split_block = block.splitlines()
    new_lines = []
    for line in split_block:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)


def paragraph_to_html_node(block: str) -> ParentNode:
    """Helper function that returns a paragraph parent node from a text block"""

    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)
