import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):

    # Equality
    def test_eq(self):
        html_node = HTMLNode("p", "work it out", ["p", "div", "a"], {"href": "https://www.bing.com", "target": "_blank"})
        html_node_2 = HTMLNode("p", "work it out", ["p", "div", "a"], {"href": "https://www.bing.com", "target": "_blank"})
        self.assertEqual(html_node, html_node_2)
    
    # Inequality
    def test_inequality(self):
        html_node = HTMLNode("p", "work it out", ["p", "div", "a"], {"href": "https://www.bing.com", "target": "_blank"})
        html_node_2 = HTMLNode("a", "work it out", ["p", "div", "a"], {"href": "https://www.bing.com", "target": "_blank"})
        self.assertNotEqual(html_node, html_node_2)

    # Testing Specific Methods
    def test_to_html(self):
        html_node = HTMLNode("p", "work it out", ["p", "div", "a"], {"href": "https://www.bing.com", "target": "_blank"})
        with self.assertRaises(NotImplementedError):
            html_node.to_html()
    
    def test_props_to_html(self):
        html_node = HTMLNode("p", "work it out", ["p", "div", "a"], {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(html_node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    # Testing Lead Nodes
    # Equality
    def test_eq_leaf_node(self):
        leaf_node = LeafNode("p", "work it out", {"href": "https://www.bing.com", "target": "_blank"})
        leaf_node_2 = LeafNode("p", "work it out", {"href": "https://www.bing.com", "target": "_blank"})
        self.assertEqual(leaf_node, leaf_node_2)
    
    # Inequality
    def test_inequality_leaf_node(self):
        leaf_node = LeafNode("p", "work it out", {"href": "https://www.bing.com", "target": "_blank"})
        leaf_node_2 = LeafNode("p", "try me buster", {"href": "https://www.bing.com", "target": "_blank"})
        self.assertNotEqual(leaf_node, leaf_node_2)

    # Props to HTML
    def test_leaf_node_props_to_html(self):
        leaf_node = LeafNode("p", "work it out", {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(leaf_node.props_to_html(), ' href="https://www.google.com" target="_blank"')
    
    # To HTML Method
    # Standard
    def test_lead_node_to_html(self):
        leaf_node = LeafNode("a", "Look at my website", {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(leaf_node.to_html(), '<a href="https://www.google.com" target="_blank">Look at my website</a>')

    # If no value passed
    def test_lead_node_to_html_no_value(self):
        leaf_node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            leaf_node.to_html()
    
    # If tag == None
    def test_lead_node_to_html_tag_none(self):
        value = "bite me spider"
        leaf_node = LeafNode(None, value)
        self.assertEqual(leaf_node.to_html(), value)

class TestLeafNode(unittest.TestCase):
    # To HTML Method
    # Standard
    def test_parent_node_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    



if __name__ == "__main__":
    unittest.main()