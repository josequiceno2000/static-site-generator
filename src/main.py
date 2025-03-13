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

def split_nodes_image(old_nodes):
    new_nodes = []
    first_part = old_nodes.text.split("!")[0]
    second_part = extract_markdown_images(old_nodes.text)[0]
    third_part = re.findall(r"\)(.*?)\!", old_nodes.text)[0]
    fourth_part = extract_markdown_images(old_nodes.text)[1]

    new_nodes.append(TextNode(first_part, TextType.NORMAL_TEXT))
    new_nodes.append(TextNode(second_part[0], TextType.IMAGES, second_part[1]))
    new_nodes.append(TextNode(third_part, TextType.NORMAL_TEXT))
    new_nodes.append(TextNode(fourth_part[0], TextType.IMAGES, fourth_part[1]))


def split_nodes_link(old_nodes):
    new_nodes = []
    first_part = old_nodes.text.split("[")[0]
    second_part = extract_markdown_links(old_nodes.text)[0]
    third_part = re.findall(r"\)(.*?)\[", old_nodes.text)[0]
    fourth_part = extract_markdown_links(old_nodes.text)[1]
    
    
    new_nodes.append(TextNode(first_part, TextType.NORMAL_TEXT))
    new_nodes.append(TextNode(second_part[0], TextType.LINK, second_part[1]))
    new_nodes.append(TextNode(third_part, TextType.NORMAL_TEXT))
    new_nodes.append(TextNode(fourth_part[0], TextType.NORMAL_TEXT, fourth_part[1]))
    



def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def main():
    my_node = TextNode("This is text with a `code block` word", TextType.NORMAL_TEXT)
    print(split_nodes_delimiter([my_node], "`", TextType.CODE_TEXT))

    node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.NORMAL_TEXT
    )
    print()
    (split_nodes_image(node))


main()

