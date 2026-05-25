from textnode import TextType
from textnode import TextNode
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if not isinstance(text_type, TextType):
        raise TypeError("Expected text_type to be of type TextType")
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(node)
        else:
            node_text_splits = node.text.split(delimiter)
            if len(node_text_splits) % 2 == 0:
                raise Exception("The markdown syntax is invalid")
            if len(node_text_splits) == 1:
                new_nodes.append(node)
                continue
            node_group = []
            for i in range(len(node_text_splits)):
                if i % 2 == 0:
                    new_node = TextNode(node_text_splits[i], TextType.PLAIN_TEXT)
                    node_group.append(new_node)
                else:
                    new_node = TextNode(node_text_splits[i], text_type)
                    node_group.append(new_node)
            new_nodes.extend(node_group)
    return new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        markdown_images = extract_markdown_images(node.text)
        if len(markdown_images) == 0:
            if node.text != "":
                new_nodes.append(node)
            continue
        text = node.text
        for image in markdown_images:
            alt_text = image[0]
            src = image[1]
            sections = text.split(f"![{alt_text}]({src})", 1)
            before = TextNode(sections[0], TextType.PLAIN_TEXT)
            img = TextNode(alt_text, TextType.IMAGE, src)
            node_group = [before, img]
            new_nodes.extend(node_group)
            text = sections[1]
        if new_nodes[len(new_nodes) - 1].text_type is TextType.IMAGE:
            if text != "":
                new_nodes.append(TextNode(text, TextType.PLAIN_TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        markdown_links = extract_markdown_links(node.text)
        if len(markdown_links) == 0:
            if node.text != "":
                new_nodes.append(node)
            continue
        text = node.text
        for link in markdown_links:
            anchor_text = link[0]
            href = link[1]
            sections = text.split(f"[{anchor_text}]({href})", 1)
            before = TextNode(sections[0], TextType.PLAIN_TEXT)
            link_node = TextNode(anchor_text, TextType.LINK, href)
            node_group = [before, link_node]
            new_nodes.extend(node_group)
            text = sections[1]
        if new_nodes[len(new_nodes) - 1].text_type is TextType.LINK:
            if text != "":
                new_nodes.append(TextNode(text, TextType.PLAIN_TEXT))
    return new_nodes


def text_to_textnodes(text):
    firstNode = TextNode(text, TextType.PLAIN_TEXT)
    split_bold_nodes = split_nodes_delimiter([firstNode], "**", TextType.BOLD)
    split_italic_nodes = split_nodes_delimiter(split_bold_nodes, "_", TextType.ITALIC)
    split_code_nodes = split_nodes_delimiter(split_italic_nodes, "`", TextType.CODE)
    split_image_nodes = split_nodes_image(split_code_nodes)
    complete_split = split_nodes_link(split_image_nodes)
    return complete_split
