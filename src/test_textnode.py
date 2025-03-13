import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):

    # Testing Equality
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)
    
    def test_eq_2(self):
        node = TextNode("This is a text node", TextType.NORMAL_TEXT)
        node2 = TextNode("This is a text node", TextType.NORMAL_TEXT)
        self.assertEqual(node, node2)

    def test_eq_3(self):
        node = TextNode("This is a text node", TextType.LINK)
        node2 = TextNode("This is a text node", TextType.LINK)
        self.assertEqual(node, node2)
    
    # Testing Inequality
    # Different Test
    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.CODE_TEXT)
        node2 = TextNode("This is a different text node", TextType.ITALIC_TEXT)
        self.assertNotEqual(node, node2)
    
    # Same text, different type
    def test_not_eq_2(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.IMAGES)
        self.assertNotEqual(node, node2)
    
    def test_not_eq_3(self):
        node = TextNode("This is a text node", TextType.NORMAL_TEXT)
        node2 = TextNode("This is a text node", TextType.ITALIC_TEXT)
        self.assertNotEqual(node, node2)

    # Testing URL defaults to None
    def test_url(self):
        node = TextNode("This is a text node", TextType.NORMAL_TEXT)
        test_url = None
        self.assertEqual(node.url, test_url)

    # Testing __eq__ method
    # Not equal
    def test_eq_method(self):
        node = TextNode("This is a text node", TextType.NORMAL_TEXT)
        node2 = TextNode("This is a text node", TextType.ITALIC_TEXT)
        self.assertEqual(node.__eq__(node2), False)
    
    # Equal
    def test_eq_method_2(self):
        node = TextNode("This is a text node", TextType.NORMAL_TEXT)
        node2 = TextNode("This is a text node", TextType.NORMAL_TEXT)
        self.assertEqual(node.__eq__(node2), True)

if __name__ == "__main__":
    unittest.main()