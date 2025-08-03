from src.copystatic import move_tree
from src.extract_markdown import generate_page

dir_path_static = "./static"
dir_path_public = "./public"


def main():
    move_tree(
        dir_path_static,
        dir_path_public,
    )
    generate_page("./content/index.md", "./template.html", "./public/index.html")


if __name__ == "__main__":
    main()
