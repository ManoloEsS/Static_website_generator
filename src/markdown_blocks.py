from enum import Enum


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
    elif all(line.startswith("- ") for line in markdown_block.split("\n")):
        return BlockType.ULIST
    elif starts_with_ascending_number(markdown_block):
        return BlockType.OLIST
    return BlockType.PARAGRAPH


def starts_with_ascending_number(markdown_block: str) -> bool:
    """Helper function to check if every line in a markdown block starts with ascending numbers followed by a '.'"""
    lines = markdown_block.split("\n")
    n = 1
    for line in lines:
        if not line.startswith(f"{n}. "):
            return False
        n += 1
    return True
