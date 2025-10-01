from enum import Enum
from src.htmlnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    """A node representing text with specific formatting type."""
    
    def __init__(self, text: str, text_type: TextType, url: str = None) -> None:
        """Initialize a text node with text, type, and optional URL.
        
        Args:
            text: The text content of the node
            text_type: The type of formatting (from TextType enum)
            url: The URL for link or image nodes (optional)
        """
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: object) -> bool:
        """Check equality with another TextNode.
        
        Args:
            other: Another object to compare with
            
        Returns:
            True if all attributes are equal, False otherwise
        """
        equal = True
        if self.text != other.text:
            equal = False
        if self.text_type != other.text_type:
            equal = False
        if self.url != other.url:
            equal = False

        return equal

    def __repr__(self) -> str:
        """Return a string representation of the TextNode for debugging.
        
        Returns:
            A string representation of the node
        """
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    """Convert a TextNode to an HTML LeafNode.
    
    Args:
        text_node: A TextNode to convert
        
    Returns:
        A LeafNode with appropriate HTML tag and attributes
        
    Raises:
        ValueError: If the text_node has an invalid text type
    """
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    else:
        raise ValueError(f"Invalid text type: {text_node.text_type}")
