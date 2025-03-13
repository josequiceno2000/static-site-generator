import unittest
import textnode
import htmlnode
from main import text_node_to_html_node, extract_markdown_images, extract_markdown_links

class TestNodetoHTML(unittest.TestCase):

    def test_node_to_html_valid_normal_text(self):
        text_node = textnode.TextNode("Hello", textnode.TextType.NORMAL_TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "Hello")
        self.assertEqual(html_node.props, None)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev)")
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    

if __name__ == "__main__":
    unittest.main()