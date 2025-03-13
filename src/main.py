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

    for node in old_nodes:
        if (not node.text) or (node.text_type != TextType.NORMAL_TEXT):
            new_nodes.append(node)
            continue

        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue

        remaining_text = node.text
        for image in images:
            image_markdown = f"![{image[0]}]({image[1]})"
            parts = remaining_text.split(image_markdown, 1)

            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.NORMAL_TEXT))

            new_nodes.append(TextNode(image[0], TextType.IMAGES, image[1]))

            remaining_text = parts[1]
        
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.NORMAL_TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if (not node.text) or (node.text_type != TextType.NORMAL_TEXT):
            new_nodes.append(node)
            continue

        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue

        remaining_text = node.text
        for link in links:
            link_markdown = f"[{link[0]}]({link[1]})"
            parts = remaining_text.split(link_markdown, 1)

            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.NORMAL_TEXT))

            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))

            remaining_text = parts[1]
        
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.NORMAL_TEXT))

    return new_nodes
    

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def main():
    my_node = TextNode("This is text with a `code block` word", TextType.NORMAL_TEXT)
    print(split_nodes_delimiter([my_node], "`", TextType.CODE_TEXT))


main()

