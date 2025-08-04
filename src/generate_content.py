from src.markdown_blocks import (
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
    markdown_to_html_node,
)
import os
from pathlib import Path


def extract_title(markdown_file) -> str:
    """Function that extracts the 'h1' header from markdown text"""

    md_blocks = markdown_to_blocks(markdown_file)
    for block in md_blocks:
        if block_to_block_type(block) == BlockType.HEADING and block.startswith("# "):
            return block.lstrip("# ").strip()
    raise ValueError("No h1 header, invalid markdown file")


def generate_page(from_path: str, template_path: str, dest_path: str):
    """Function that creates an HTML file at the destinaton path using the content from a path and the
    specified template"""

    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as md:
        md_contents = md.read()

    with open(template_path, "r") as template:
        html_content = template.read()

    node = markdown_to_html_node(md_contents)
    html = node.to_html()
    title = extract_title(md_contents)
    html_content = html_content.replace("{{ Title }}", title)
    html_content = html_content.replace("{{ Content }}", html)

    write_html_file(dest_path, html_content)


def generate_pages_recursive(
    dir_path_content: str, template_path: str, dest_dir_path: str
):
    """Function that crawls through the source directory, generates and writes html
    files into the destination path for every markdown file"""

    dir_content = os.listdir(dir_path_content)
    for path in dir_content:
        current_path = os.path.join(dir_path_content, path)
        dest_path = os.path.join(dest_dir_path, path)
        if os.path.isfile(current_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(current_path, template_path, dest_path)
            continue
        generate_pages_recursive(current_path, template_path, dest_path)


def write_html_file(dest_path: str, html_content: str):
    """Function that creates the destination dir for the"""
    path, file_name = os.path.split(dest_path)
    os.makedirs(path, exist_ok=True)
    with open(dest_path, "w") as html:
        html.write(html_content)
