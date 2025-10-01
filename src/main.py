from src.copystatic import move_tree
from src.generate_content import generate_pages_recursive
import sys


dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
dir_path_docs = "./docs"


def main() -> None:
    """Main entry point for the static site generator.
    
    Copies static files to the docs directory and generates HTML pages
    from markdown content. Optionally accepts a basepath argument from
    command line for configuring URL paths.
    """
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    move_tree(
        dir_path_static,
        dir_path_docs,
    )
    generate_pages_recursive(
        dir_path_content, "./template.html", dir_path_docs, basepath
    )


if __name__ == "__main__":
    main()
