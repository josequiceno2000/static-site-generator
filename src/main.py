import re
from textnode import TextNode, TextType
from htmlnode import LeafNode, ParentNode, HTMLNode

def text_node_to_html_node(text_node):
    match (text_node.text_type):
        case (TextType.NORMAL_TEXT):
            value = text_node.text
            return LeafNode(None, value)
        case (TextType.BOLD_TEXT):
            value = text_node.text
            return LeafNode("b", value)
        case (TextType.ITALIC_TEXT):
            value = text_node.text
            return LeafNode("i", value)
        case (TextType.CODE_TEXT):
            value = text_node.text
            return LeafNode("code", value)
        case (TextType.LINK):
            value = text_node.text
            url = text_node.url
            return LeafNode("a", value, {"href": f"{url}"})
        case (TextType.IMAGES):
            alt = text_node.text
            src = text_node.url
            return LeafNode("img", "", {"src": f"{src}", "alt": f"{alt}"})
        case _:
            raise Exception("not a valid text type")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        node_sections = node.text.split(delimiter)
        node_text_type = node.text_type
        for text in node_sections:
            if node_sections.index(text) % 2 != 0:
                new_nodes.append(TextNode(text, text_type))
            else:
                new_nodes.append(TextNode(text, node_text_type))
        return(new_nodes)

def extract_markdown_images(text):
    alt_text_tuple = re.findall(r"\[(.*?)\]", text)
    link_tuple = re.findall(r"\((.*?)\)", text)
    
    my_list = []
    for alt, link in zip(alt_text_tuple, link_tuple):
        my_list.append(alt)
        my_list.append(link)
    
    return my_list

def main():
    my_node = TextNode("This is text with a `code block` word", TextType.NORMAL_TEXT)
    print(split_nodes_delimiter([my_node], "`", TextType.CODE_TEXT))
    text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    print(extract_markdown_images(text))

main()

