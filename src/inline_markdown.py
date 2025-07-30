import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
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


def split_nodes_image(old_nodes: list) -> list:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if len(node.text) == 0:
            continue
        image_markdown = extract_markdown_images(node.text)
        if len(image_markdown) == 0:
            new_nodes.append(node)

        text_to_check = node.text
        current_node = []
        for image in image_markdown:
            split_node_text = text_to_check.split(f"![{image[0]}]({image[1]})", 1)
            before = split_node_text[0]
            after = split_node_text[1]
            if before != "":
                current_node.append(TextNode(before, TextType.TEXT))
            current_node.append(TextNode(image[0], TextType.IMAGE, image[1]))
            text_to_check = after
        if text_to_check != "":
            current_node.append(TextNode(text_to_check, TextType.TEXT))
        new_nodes.extend(current_node)


def split_nodes_link(old_nodes: list) -> list:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if len(node.text) == 0:
            continue
        link_markdown = extract_markdown_links(node.text)
        if len(link_markdown) == 0:
            new_nodes.append(node)

        text_to_check = node.text
        current_node = []
        for link in link_markdown:
            split_node_text = text_to_check.split(f"[{link[0]}]({link[1]})", 1)
            before = split_node_text[0]
            after = split_node_text[1]
            if before != "":
                current_node.append(TextNode(before, TextType.TEXT))
            current_node.append(TextNode(link[0], TextType.LINK, link[1]))
            text_to_check = after
        if text_to_check != "":
            current_node.append(TextNode(text_to_check, TextType.TEXT))
        new_nodes.extend(current_node)


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    image_matches = re.findall(pattern, text)
    return image_matches


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    link_matches = re.findall(pattern, text)
    return link_matches
