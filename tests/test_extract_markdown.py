import unittest
from src.extract_markdown import extract_title


class TestMarkdown(unittest.TestCase):
    def test_markdown_extract_header(self):
        content = "# Hello"
        header = extract_title(content)
        self.assertEqual(header, "Hello")


if __name__ == "__main__":
    unittest.main()
