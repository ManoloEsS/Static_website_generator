import os
import shutil


def move_tree(source_path: str, destination_path: str):
    """Function that moves directories and files from a source path into a destination path"""

    print("Deleting public directory...")
    if os.path.exists(destination_path):
        shutil.rmtree(destination_path)
    print("Copying static files to public directory...")
    print("Source directory structure: ")
    print_tree(source_path)
    print()
    recursive_copy(source_path, destination_path)
    print(
        f"{source_path} and all contained directories have been copied to {destination_path}"
    )
    print()


def recursive_copy(source_path: str, destination_path: str):
    """Function that recursively copies a directory tree into a destination directory"""

    if not os.path.exists(destination_path):
        os.mkdir(destination_path)
    print(f"Created new directory {destination_path}")
    print()
    dir_contents = os.listdir(source_path)
    for path in dir_contents:
        current_path = os.path.join(source_path, path)
        new_path = os.path.join(destination_path, path)
        if os.path.isfile(current_path):
            shutil.copy(current_path, new_path)
            print(f"Copied {current_path} -> {new_path}")
            print()
            continue
        recursive_copy(current_path, new_path)


def print_tree(root_dir):
    """Function that prints a directory's tree structure"""
    for dirpath, dirnames, filenames in os.walk(root_dir):
        depth = dirpath[len(root_dir) :].count(os.sep)
        indent = "    " * depth
        print(f"{indent}{os.path.basename(dirpath)}/")
        subindent = "    " * (depth + 1)
        for fname in filenames:
            print(f"{subindent}{fname}")
