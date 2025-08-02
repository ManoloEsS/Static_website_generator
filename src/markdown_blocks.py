import textwrap
import re
from enum import Enum
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import text_to_textnodes


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

    if markdown_block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    elif markdown_block.startswith("```") and markdown_block.endswith("```"):
        return BlockType.CODE
    elif all(line.startswith("> ") for line in markdown_block.split("\n")):
        return BlockType.QUOTE
    elif all(line.startswith(("- ", "* ")) for line in markdown_block.split("\n")):
        return BlockType.ULIST
    elif starts_with_ascending_number(markdown_block):
        return BlockType.OLIST
    return BlockType.PARAGRAPH


def starts_with_ascending_number(markdown_block: str) -> bool:
    """Helper function to check if every line in a markdown block starts with ascending numbers followed by '. '"""

    lines = markdown_block.split("\n")
    n = 1
    for line in lines:
        if not line.startswith(f"{n}. "):
            return False
        n += 1
    return True


def markdown_to_html_node(markdown: str, root_tag="div") -> HTMLNode:
    """Function that converts a full markdown document into a parent HTMLnode with multiple children"""

    markdown_blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in markdown_blocks:
        block_type = block_to_block_type(block)
        tag = block_type_to_node_tag(block_type)

        if block_type == BlockType.CODE:
            nodes.append(code_text_to_parent_html(block))
            continue
        if block_type == BlockType.ULIST:
            children = unordered_list_to_children_nodes(block)
            nodes.append(ParentNode(tag, children))
            continue
        if block_type == BlockType.OLIST:
            children = ordered_list_to_children_nodes(block)
            nodes.append(ParentNode(tag, children))
            continue
        if block_type == BlockType.HEADING:
            tag += str(get_header_number(block))
            children = header_to_children_nodes(block)
            nodes.append(ParentNode(tag, children))
            continue
        if block_type == BlockType.QUOTE:
            children = quote_to_children_nodes(block)
            nodes.append(ParentNode(tag, children))
            continue
        children = text_to_children(block)
        nodes.append(ParentNode(tag, children))

    return ParentNode(root_tag, nodes)


def text_to_children(text: str) -> list[LeafNode]:
    """Helper function that takes a string and returns a list of HTMLNodes"""

    children_nodes = []
    text_nodes = text_to_textnodes(text)
    for node in text_nodes:
        new_html_node = text_node_to_html_node(node)
        children_nodes.append(new_html_node)
    return children_nodes


def block_type_to_node_tag(block_type: BlockType) -> str:
    """Helper function that returns the tag for an HTMLNode from markdown"""

    if block_type == BlockType.QUOTE:
        return "blockquote"
    elif block_type == BlockType.HEADING:
        return "h"
    elif block_type == BlockType.ULIST:
        return "ul"
    elif block_type == BlockType.OLIST:
        return "ol"
    elif block_type == BlockType.CODE:
        return "code"
    return "p"


def get_header_number(block: str) -> int:
    """Helper function that returns the number of '#' to determine the number in the heading tag"""
    return block.count("#")


def code_text_to_parent_html(block: str) -> ParentNode:
    """Helper function that takes a code block and creates a parent node
    with the 'pre' tag that nests the code html node"""

    lines = block.splitlines()
    content_lines = lines[1:-1]
    dedented = textwrap.dedent("\n".join(content_lines))
    code_content = dedented + "\n"
    code_text_node = TextNode(code_content, TextType.CODE)
    code_html_node = text_node_to_html_node(code_text_node)
    return ParentNode("pre", [code_html_node])


def unordered_list_to_children_nodes(block: str) -> list[ParentNode]:
    """Helper function that returns a list of unordered list item Parent nodes from a text block"""

    split_block = block.split("\n")
    formatted_block = [block[2:] for block in split_block]
    list_items = []
    for block in formatted_block:
        html_children = text_to_children(block)
        list_items.append(ParentNode("li", html_children))
    return list_items


def ordered_list_to_children_nodes(block: str) -> list[ParentNode]:
    """Helper function that returns a list of ordered list item Parent nodes from a text block"""

    split_block = block.split("\n")
    formatted_block = [block[block.find(".") + 2 :] for block in split_block]
    list_items = []
    for block in formatted_block:
        html_children = text_to_children(block)
        list_items.append(ParentNode("li", html_children))
    return list_items


def header_to_children_nodes(block: str) -> list[ParentNode]:
    """Helper function that returns a list of header Parent nodes from a text block"""

    formatted_block = re.sub(r"^#{1,6}\s*", "", block)
    header_children = text_to_children(formatted_block)
    return header_children


def quote_to_children_nodes(block: str) -> list[ParentNode]:
    """Helper function that returns a list of quote parent nodes from a text block"""

    split_block = block.splitlines()
    formatted_block = [block[2:] for block in split_block]
    inner_markdown = "\n".join(formatted_block)
    quote_parent = markdown_to_html_node(inner_markdown)
    return quote_parent.children
