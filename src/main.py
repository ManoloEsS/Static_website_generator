from src.copystatic import move_tree
from src.generate_content import generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"


def main():
    move_tree(
        dir_path_static,
        dir_path_public,
    )
    generate_pages_recursive(dir_path_content, "./template.html", dir_path_public)


if __name__ == "__main__":
    main()
