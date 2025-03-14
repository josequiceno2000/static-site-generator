import re
from enum import Enum
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
        if node.text_type != TextType.NORMAL_TEXT:
            new_nodes.append(node)
            continue

        node_sections = node.text.split(delimiter)
        for i, text in enumerate(node_sections):
            if i % 2 != 0:
                new_nodes.append(TextNode(text, text_type))
            elif text:
                new_nodes.append(TextNode(text, TextType.NORMAL_TEXT))
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

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.NORMAL_TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD_TEXT)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC_TEXT)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE_TEXT)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown): 
    lines = markdown.split("\n\n")
    stripped_lines = [line.strip("\n    ") for line in lines]
    cleaned_lines = [line.replace("\n    ", "\n") for line in stripped_lines]
    return cleaned_lines

# Block Types
class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(markdown):
    lines = markdown.split("\n")
    
    if markdown.startswith("```") and markdown.endswith("```"):
        return BlockType.CODE
    elif re.match(r"^(#{1,6}) ", markdown):
        return BlockType.HEADING
    elif all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    elif all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    elif is_consecutive_ordered_list(lines):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

def is_consecutive_ordered_list(lines):
    lines = [line.strip() for line in lines if line.strip()]
    if not lines:
        return False
    
    expected_number = 1
    for line in lines:
        match = re.match(r"^(\d+)\. ", line)
        if not match:
            return False
        number = int(match.group(1))
        if number != expected_number:
            return False
        expected_number += 1
    return True

def main():
    pass
    

main()

