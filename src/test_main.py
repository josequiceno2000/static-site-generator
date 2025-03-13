import unittest
import textnode
import htmlnode
from main import text_node_to_html_node

class TestNodetoHTML(unittest.TestCase):

    def test_node_to_html_valid_normal_text(self):
        text_node = textnode.TextNode("Hello", textnode.TextType.NORMAL_TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "Hello")
        self.assertEqual(html_node.props, None)

    

if __name__ == "__main__":
    unittest.main()