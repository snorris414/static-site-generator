from io import UnsupportedOperation
from htmlnode import HTMLNode
from split_blocks import markdown_to_blocks
from blocktype import block_to_block_type, BlockType
from splitnodes_delim import text_to_textnodes
from textnode import TextNode, text_node_to_html_node, TextType
from parentnode import ParentNode
import re


def markdown_to_html_node(markdown):
    children = []
    markdown_blocks = markdown_to_blocks(markdown)
    for block in markdown_blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.HEADING:
                children.append(generate_heading_html(block))
            case BlockType.CODE:
                children.append(generate_code_block_html(block))
            case BlockType.QUOTE:
                children.append(generate_quote_html(block))
            case BlockType.UNORDERED_LIST:
                children.append(generate_unordered_list_html(block))
            case BlockType.ORDERED_LIST:
                children.append(generate_ordered_list_html(block))
            case BlockType.PARAGRAPH:
                children.append(generate_paragraph_html(block))
            case _:
                raise UnsupportedOperation(
                    f"Unknown block type not supported: {block_type}"
                )
    return ParentNode("div", children)


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = list(map(lambda x: text_node_to_html_node(x), text_nodes))
    return html_nodes


def generate_heading_html(text):
    i = 0
    while text[i] == "#":
        i += 1

    heading = None
    match i:
        case 1:
            heading = "h1"
        case 2:
            heading = "h2"
        case 3:
            heading = "h3"
        case 4:
            heading = "h4"
        case 5:
            heading = "h5"
        case 6:
            heading = "h6"
        case _:
            raise Exception("Heading could not be parsed into a valid html tag")

    heading_text = text[i + 1 :]
    children = text_to_children(heading_text)
    if len(children) > 0:
        return ParentNode(heading, children, None)
    return HTMLNode(heading, heading_text)


def generate_quote_html(text):
    quote_text = " ".join(
        list(map(lambda x: x.removeprefix(">").strip(), text.splitlines()))
    )
    children = text_to_children(quote_text)

    if len(children) > 0:
        return ParentNode("blockquote", children, None)
    return HTMLNode("blockquote", quote_text)


def generate_unordered_list_html(text):
    list_items = text.splitlines()
    list_items = list(map(lambda x: x.removeprefix("- "), list_items))

    list_item_html_list = []
    for item in list_items:
        children = text_to_children(item)
        list_item = None
        if len(children) > 0:
            list_item = ParentNode("li", children)
        else:
            list_item = HTMLNode("li", item)
        list_item_html_list.append(list_item)

    return ParentNode("ul", list_item_html_list)


def generate_ordered_list_html(text):
    list_items = text.splitlines()
    list_items = list(map(lambda x: re.sub(r"^\d+\.\s", "", x), list_items))

    list_item_html_list = []
    for item in list_items:
        children = text_to_children(item)
        list_item = None
        if len(children) > 0:
            list_item = ParentNode("li", children)
        else:
            list_item = HTMLNode("li", item)
        list_item_html_list.append(list_item)

    return ParentNode("ol", list_item_html_list)


def generate_code_block_html(text):
    text = text.replace("```", "").lstrip()
    text_node = TextNode(text, TextType.CODE)
    code_html_node = text_node_to_html_node(text_node)
    return ParentNode("pre", [code_html_node])


def generate_paragraph_html(text):
    text = text.replace("\n", " ")
    children = text_to_children(text)
    if len(children) > 0:
        return ParentNode("p", children)
    return HTMLNode("p", text)
