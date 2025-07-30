from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if node.text.count(delimiter) % 2 != 0:
            raise SyntaxError("Invalid Markdown syntax")

        split_node_text = node.text.split(delimiter)
        for i, item in enumerate(split_node_text):
            if item == "":
                continue
            if i % 2 != 0:
                new_nodes.append(TextNode(item, text_type))
                continue
            new_nodes.append(TextNode(item, TextType.TEXT))

    return new_nodes
