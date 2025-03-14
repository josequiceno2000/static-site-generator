import re
import os
import shutil
import logging
import sys
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

def text_to_children(text):
    """Convert a string of text to a list of HTMLNodes by parsing markdown"""
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)

        if isinstance(html_node, LeafNode) and not html_node.value:
            print(f"Warning: Skipping leaf node with no value: {html_node}")
            continue

        html_nodes.append(html_node)
    return html_nodes

def process_paragraph(block):
    children = text_to_children(block)

    if not children:
        children = [LeafNode(None, block)]

    return ParentNode("p", children)

def process_heading(block):
    match = re.match(r"^(#{1,6}) (.+)$", block)

    if not match:
        return ParentNode("h1", [LeafNode(None, block)])

    level = len(match.group(1))
    text = match.group(2)
    children = text_to_children(text)

    if not children:
        children = [LeafNode(None, text)]

    return ParentNode(f"h{level}", children)

def process_code(block):
    lines = block.split("\n")
    if len(lines) >= 2 and lines[0].startswith("```") and lines[-1].endswith("```"):
        content = "\n".join(lines[1:-1])
    else:
        content = block.strip("`").strip()

    if not content:
        content = " "

    code_node = LeafNode("code", content)

    return ParentNode("pre", [code_node])

def process_quote(block):
    """Convert a quote block to an HTMLNode."""
    # Remove the > marker from each line
    lines = block.split("\n")
    clean_lines = [line[1:].strip() if line.startswith('>') else line.strip() for line in lines]
    clean_text = "\n".join(clean_lines)
    
    children = text_to_children(clean_text)
    # Make sure we have at least one child
    if not children:
        children = [LeafNode(None, clean_text)]
    return ParentNode("blockquote", children)

def process_unordered_list(block):
    """Convert an unordered list block to an HTMLNode."""
    lines = block.split("\n")
    list_items = []
    
    for line in lines:
        if line.strip():
            # Remove the "- " marker
            text = line[2:].strip() if line.startswith("- ") else line.strip()
            children = text_to_children(text)
            # Make sure we have at least one child
            if not children:
                children = [LeafNode(None, text)]
            list_items.append(ParentNode("li", children))
    
    # Make sure we have at least one item
    if not list_items:
        list_items = [ParentNode("li", [LeafNode(None, "")])]
    
    return ParentNode("ul", list_items)

def process_ordered_list(block):
    lines = block.split("\n")
    list_items = []
    
    for line in lines:
        if line.strip():
            # Remove the "number. " marker
            text = re.sub(r"^\d+\.\s*", "", line).strip()
            children = text_to_children(text)
            # Make sure we have at least one child
            if not children:
                children = [LeafNode(None, text)]
            list_items.append(ParentNode("li", children))
    
    # Make sure we have at least one item
    if not list_items:
        list_items = [ParentNode("li", [LeafNode(None, "")])]
    
    return ParentNode("ol", list_items)


def markdown_to_html_node(markdown):
    """Convert a markdown string to a single HTMLNode object"""
    blocks = markdown_to_blocks(markdown)
    block_nodes = []

    for block in blocks:
        if not block.strip():
            continue

        block_type = block_to_block_type(block)

        try:
            match block_type:
                case BlockType.PARAGRAPH:
                    block_nodes.append(process_paragraph(block))
                case BlockType.HEADING:
                    block_nodes.append(process_heading(block))
                case BlockType.CODE:
                    block_nodes.append(process_code(block))
                case BlockType.QUOTE:
                    block_nodes.append(process_quote(block))
                case BlockType.UNORDERED_LIST:
                    block_nodes.append(process_unordered_list(block))
                case BlockType.ORDERED_LIST:
                    block_nodes.append(process_ordered_list(block))
        except Exception as e:
            print(f"Error processing block of type {block_type}: {e}")
            print(f"Block content: {block}")

            block_nodes.append(ParentNode("p", [LeafNode(None, block)]))

    if not block_nodes:
        block_nodes = [ParentNode("p", [LeafNode(None, "Empty markdown document")])]

    return ParentNode("div", block_nodes)     

def copy_directory(source_dir, dest_dir):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

    if not os.path.exists(source_dir):
        logging.error(f"Source directory '{source_dir}' does not exist!")
        return
    
    if os.path.exists(dest_dir):
        logging.info(f"Deleting contents of '{dest_dir}'")
        for item in os.listdir(dest_dir):
            item_path = os.path.join(dest_dir, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
                logging.info(f"Deleted file: {item_path}")
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
                logging.info(f"Deleted directory: {item_path}")
    
    else:
        os.makedirs(dest_dir)
        logging.info(f"Created destination directory: {dest_dir}")

    _copy_contents(source_dir, dest_dir)

    logging.info(f"Copy finalized: '{source_dir}' -> '{dest_dir}'")

def _copy_contents(src, dst):
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)

        if os.path.isfile(src_path):
            shutil.copy2(src_path, dst_path)
            logging.info(f"Copied file: {src_path} to {dst_path}")
        elif os.path.isdir(src_path):
            if not os.path.exists(dst_path):
                os.makedirs(dst_path)
                logging.info(f"Created new directory: {dst_path}")
            _copy_contents(src_path, dst_path)

def extract_title(markdown):
    match = re.search(r"^#\s+(.+)$", markdown, re.MULTILINE)
    if match:
        return match.group(1).strip()
    else:
        raise Exception("No h1 header found!")
    
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # Read the markdown file
    with open(from_path, 'r', encoding='utf-8') as md_file:
        markdown_content = md_file.read()
    
    # Read the template file
    with open(template_path, 'r', encoding='utf-8') as template_file:
        template_content = template_file.read()
    
    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    
    try:
        html_content = html_node.to_html()
    except ValueError as e:
        print(f"Error generating HTML: {e}")
        print("Falling back to simple HTML generation")
        html_content = f"<div><p>Error converting markdown to HTML: {e}</p></div>"
    
    # Extract title
    try:
        title = extract_title(markdown_content)
    except Exception as e:
        print(f"Error extracting title: {e}")
        title = "Untitled Page"
    
    # Replace placeholders in template
    final_html = template_content.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", html_content)
    
    # Create destination directory if it doesn't exist
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    # Write the final HTML to the destination file
    with open(dest_path, 'w', encoding='utf-8') as dest_file:
        dest_file.write(final_html)
    
    print(f"Successfully generated {dest_path}")

def main():
    try:
        print(f"Now beggining static site generation...")
        copy_directory("static", "public")
        generate_page(
            from_path="content/index.md",
            template_path="template.html",
            dest_path="public/index.html"
        )

        print("Static site generated!")
    except Exception as e:
        print(f"Error during site generation: {e}")
        sys.exit(1)
    

main()

