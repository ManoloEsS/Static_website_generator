from src.markdown_blocks import (
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
    markdown_to_html_node,
)
import os
from pathlib import Path


def extract_title(markdown_file: str) -> str:
    """Function that extracts the 'h1' header from markdown text.
    
    Args:
        markdown_file: A string containing markdown text
        
    Returns:
        The text of the h1 header without the '#' prefix
        
    Raises:
        ValueError: If no h1 header is found in the markdown
    """
    md_blocks = markdown_to_blocks(markdown_file)
    for block in md_blocks:
        if block_to_block_type(block) == BlockType.HEADING and block.startswith("# "):
            return block.lstrip("# ").strip()
    raise ValueError("No h1 header, invalid markdown file")


def generate_page(
    from_path: str, template_path: str, dest_path: str, basepath: str = "/"
) -> None:
    """Function that creates an HTML file at the destinaton path using the content from a path and the
    specified template.
    
    Args:
        from_path: Path to the source markdown file
        template_path: Path to the HTML template file
        dest_path: Path where the output HTML file will be created
        basepath: Base path for URLs in the HTML (default: "/")
    """
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
    html_content = html_content.replace('href="/', f'href="{basepath}')
    html_content = html_content.replace('src="/', f'src="{basepath}')

    write_html_file(dest_path, html_content)


def generate_pages_recursive(
    dir_path_content: str, template_path: str, dest_dir_path: str, basepath: str = "/"
) -> None:
    """Function that crawls through the source directory, generates and writes html
    files into the destination path for every markdown file.
    
    Args:
        dir_path_content: Path to the source directory containing markdown files
        template_path: Path to the HTML template file
        dest_dir_path: Path to the destination directory for generated HTML files
        basepath: Base path for URLs in the HTML (default: "/")
    """
    dir_content = os.listdir(dir_path_content)
    for path in dir_content:
        current_path = os.path.join(dir_path_content, path)
        dest_path = os.path.join(dest_dir_path, path)
        if os.path.isfile(current_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(current_path, template_path, dest_path, basepath)
            continue
        generate_pages_recursive(current_path, template_path, dest_path, basepath)


def write_html_file(dest_path: str, html_content: str) -> None:
    """Function that creates the destination directory and writes the HTML content to a file.
    
    Args:
        dest_path: The destination file path for the HTML file
        html_content: The HTML content to write to the file
    """
    path, file_name = os.path.split(dest_path)
    os.makedirs(path, exist_ok=True)
    with open(dest_path, "w") as html:
        html.write(html_content)
