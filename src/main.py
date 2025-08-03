from .textnode import TextNode, TextType


def main():
    new_node = TextNode("hello", TextType.LINK, "boot.dev")
    print(new_node)


if __name__ == "__main__":
    main()
