import unittest
import textnode
import htmlnode
from main import text_node_to_html_node, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link

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

    
    def test_split_images(self):
        node = textnode.TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            textnode.TextType.NORMAL_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                textnode.TextNode("This is text with an ", textnode.TextType.NORMAL_TEXT, None),
                textnode.TextNode("image", textnode.TextType.IMAGES, "https://i.imgur.com/zjjcJKZ.png"),
                textnode.TextNode(" and another ", textnode.TextType.NORMAL_TEXT, None),
                textnode.TextNode(
                    "second image", textnode.TextType.IMAGES, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = textnode.TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            textnode.TextType.NORMAL_TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                textnode.TextNode("This is text with a link ", textnode.TextType.NORMAL_TEXT, None),
                textnode.TextNode("to boot dev", textnode.TextType.LINK, "https://www.boot.dev"),
                textnode.TextNode(" and ", textnode.TextType.NORMAL_TEXT, None),
                textnode.TextNode(
                    "to youtube", textnode.TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

if __name__ == "__main__":
    unittest.main()