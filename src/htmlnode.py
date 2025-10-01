class HTMLNode:
    """Base class for HTML nodes in the document tree."""
    
    def __init__(
        self,
        tag: str = None,
        value: str = None,
        children: list = None,
        props: dict = None,
    ) -> None:
        """Initialize an HTML node with optional tag, value, children, and properties.
        
        Args:
            tag: The HTML tag name (e.g., 'div', 'p', 'a')
            value: The text content of the node
            children: A list of child HTMLNode objects
            props: A dictionary of HTML attributes
        """
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        """Convert the node to an HTML string.
        
        Returns:
            An HTML string representation of the node
            
        Raises:
            NotImplementedError: Must be implemented by subclasses
        """
        raise NotImplementedError

    def props_to_html(self) -> str:
        """Convert the node's properties dictionary to an HTML attribute string.
        
        Returns:
            A string of HTML attributes (e.g., ' href="url" class="btn"')
        """
        if self.props is None:
            return ""
        html_string = ""
        for key, value in self.props.items():
            html_string += f' {key}="{value}"'
        return html_string

    def __eq__(self, other: object) -> bool:
        """Check equality with another HTMLNode.
        
        Args:
            other: Another object to compare with
            
        Returns:
            True if all attributes are equal, False otherwise
        """
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        )

    def __repr__(self) -> str:
        """Return a string representation of the HTMLNode for debugging.
        
        Returns:
            A string representation of the node
        """
        return f"HTML node=(tag:{self.tag}, value:{self.value}, children:{self.children}, props:{self.props})"


class LeafNode(HTMLNode):
    """A leaf node in the HTML tree with no children, only a value."""
    
    def __init__(self, tag: str, value: str, props: dict = None) -> None:
        """Initialize a leaf node with a tag, value, and optional properties.
        
        Args:
            tag: The HTML tag name (e.g., 'p', 'span', 'b')
            value: The text content of the node
            props: A dictionary of HTML attributes
        """
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        """Convert the leaf node to an HTML string.
        
        Returns:
            An HTML string representation of the leaf node
            
        Raises:
            ValueError: If the node has no value
        """
        if self.value is None:
            raise ValueError("Invalid HTML: no value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        """Return a string representation of the LeafNode for debugging.
        
        Returns:
            A string representation of the node
        """
        return f"LeafNode:(tag:{self.tag}, value:{self.value}, props:{self.props})"


class ParentNode(HTMLNode):
    """A parent node in the HTML tree that contains child nodes."""
    
    def __init__(self, tag: str, children: list, props: dict = None) -> None:
        """Initialize a parent node with a tag, children, and optional properties.
        
        Args:
            tag: The HTML tag name (e.g., 'div', 'ul', 'p')
            children: A list of child HTMLNode objects
            props: A dictionary of HTML attributes
        """
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        """Convert the parent node and all its children to an HTML string.
        
        Returns:
            An HTML string representation of the parent node with nested children
            
        Raises:
            ValueError: If the node has no tag or no children
        """
        if self.tag is None:
            raise ValueError("Invalid HTML: no tag")
        if self.children is None or len(self.children) == 0:
            raise ValueError("Invalid HTML: no children")
        nested_html = ""
        for node in self.children:
            nested_html += node.to_html()
        return f"<{self.tag}{self.props_to_html()}>{nested_html}</{self.tag}>"

    def __repr__(self) -> str:
        """Return a string representation of the ParentNode for debugging.
        
        Returns:
            A string representation of the node
        """
        return (
            f"ParentNode:(tag:{self.tag}, children:{self.children}, props:{self.props})"
        )
