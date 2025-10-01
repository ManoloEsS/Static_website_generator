import re
from src.textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    """Split text nodes by a delimiter and apply formatting to delimited text.
    
    Args:
        old_nodes: A list of TextNode objects to process
        delimiter: The delimiter string to split on (e.g., '**', '*', '`')
        text_type: The TextType to apply to delimited text
        
    Returns:
        A new list of TextNode objects with formatting applied
        
    Raises:
        ValueError: If the markdown syntax is invalid (unmatched delimiters)
    """
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if node.text.count(delimiter) % 2 != 0:
            raise ValueError("Invalid Markdown syntax")

        current_node = []
        split_node_text = node.text.split(delimiter)
        for i, item in enumerate(split_node_text):
            if item == "":
                continue
            if i % 2 != 0:
                current_node.append(TextNode(item, text_type))
                continue
            current_node.append(TextNode(item, TextType.TEXT))
        new_nodes.extend(current_node)

    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    """Split text nodes to extract image markdown syntax.
    
    Args:
        old_nodes: A list of TextNode objects to process
        
    Returns:
        A new list of TextNode objects with images extracted
    """
    return split_nodes_link_image(old_nodes, TextType.IMAGE)


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    """Split text nodes to extract link markdown syntax.
    
    Args:
        old_nodes: A list of TextNode objects to process
        
    Returns:
        A new list of TextNode objects with links extracted
    """
    return split_nodes_link_image(old_nodes, TextType.LINK)


def split_nodes_link_image(old_nodes: list[TextNode], text_type: TextType) -> list[TextNode]:
    """Split text nodes to extract link or image markdown syntax.
    
    Args:
        old_nodes: A list of TextNode objects to process
        text_type: Either TextType.LINK or TextType.IMAGE
        
    Returns:
        A new list of TextNode objects with links or images extracted
        
    Raises:
        ValueError: If text_type is not LINK or IMAGE, or if markdown syntax is invalid
    """
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if len(node.text) == 0:
            continue

        if text_type == TextType.LINK:
            markdown = extract_markdown_links(node.text)
        elif text_type == TextType.IMAGE:
            markdown = extract_markdown_images(node.text)
        else:
            raise ValueError("Not valid text type")

        if len(markdown) == 0:
            new_nodes.append(node)
            continue

        text_to_check = node.text
        new_nodes_for_current = []

        for item in markdown:
            if text_type == TextType.LINK:
                split_node_text = text_to_check.split(f"[{item[0]}]({item[1]})", 1)
            elif text_type == TextType.IMAGE:
                split_node_text = text_to_check.split(f"![{item[0]}]({item[1]})", 1)

            if len(split_node_text) != 2:
                raise ValueError("invalid markdown syntax")

            before = split_node_text[0]
            after = split_node_text[1]
            if not re.fullmatch(r"\s*", before):
                new_nodes_for_current.append(TextNode(before, TextType.TEXT))

            if text_type == TextType.LINK:
                new_nodes_for_current.append(TextNode(item[0], TextType.LINK, item[1]))
            elif text_type == TextType.IMAGE:
                new_nodes_for_current.append(TextNode(item[0], TextType.IMAGE, item[1]))

            text_to_check = after
        if not re.fullmatch(r"\s*", text_to_check):
            new_nodes_for_current.append(TextNode(text_to_check, TextType.TEXT))
        new_nodes.extend(new_nodes_for_current)

    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    """Extract image markdown syntax from text.
    
    Args:
        text: A string containing markdown text
        
    Returns:
        A list of tuples containing (alt_text, image_url) for each image found
    """
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    image_matches = re.findall(pattern, text)
    return image_matches


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    """Extract link markdown syntax from text.
    
    Args:
        text: A string containing markdown text
        
    Returns:
        A list of tuples containing (link_text, url) for each link found
    """
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    link_matches = re.findall(pattern, text)
    return link_matches


def text_to_textnodes(text: str) -> list[TextNode]:
    """Convert markdown text into a list of TextNode objects with appropriate formatting.
    
    Args:
        text: A string containing markdown text with formatting
        
    Returns:
        A list of TextNode objects representing the formatted text
    """
    unprocessed_text_node = [TextNode(text, TextType.TEXT)]
    split_images = split_nodes_image(unprocessed_text_node)
    split_links = split_nodes_link(split_images)
    split_code = split_nodes_delimiter(split_links, "`", TextType.CODE)
    split_italic = split_nodes_delimiter(split_code, "_", TextType.ITALIC)
    split_bold = split_nodes_delimiter(split_italic, "**", TextType.BOLD)
    return split_bold
