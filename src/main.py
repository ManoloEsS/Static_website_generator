from copystatic import move_tree

dir_path_static = "./static"
dir_path_public = "./public"


def main():
    move_tree(
        dir_path_static,
        dir_path_public,
    )


if __name__ == "__main__":
    main()
