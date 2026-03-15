import re
from blocktype import markdown_to_blocks, block_to_block_type, BlockType
from textnode import text_node_to_html_node
from parse_text import text_to_textnodes
from htmlnode import ParentNode, LeafNode


def markdown_to_html_node(markdown):

    r_md_blocks = markdown_to_blocks(markdown)
    html_blocks = []
    for block in r_md_blocks:
        match block_to_block_type(block):
            case BlockType.PARAGRAPH:
                node = ParentNode("p", text_to_children(block))
                html_blocks.append(node)
            case BlockType.HEADING:
                node = ParentNode(f"h{block.count('#')}", hl_to_children(block))
                html_blocks.append(node)
            case BlockType.CODE:
                node = LeafNode("code", block.strip("```"))
                html_blocks.append(node)
            case BlockType.QUOTE:
                node = ParentNode("blockquote", q_text_to_children(block))
                html_blocks.append(node)
            case BlockType.UNORDERED_LIST:
                node = ul(block)
                html_blocks.append(node)
            case BlockType.ORDERED_LIST:
                node = ol(block)
                html_blocks.append(node)

    return ParentNode("div", html_blocks)

def q_text_to_children(text):
    return [text_node_to_html_node(node) for node in text_to_textnodes(text.lstrip("> "))]


def hl_to_children(text):
    return [text_node_to_html_node(node) for node in text_to_textnodes(text.lstrip("#").strip())]


def text_to_children(text):
    return [text_node_to_html_node(node) for node in text_to_textnodes(text)]

def ul(block):
    lines = [ParentNode("li", text_to_children(line.lstrip("-").strip())) for line in block.split("\n")]
    return ParentNode("ul", lines)
def ol(block):
    lines = [ParentNode("li", text_to_children(re.sub(r"\d\. ", "", line, 1))) for line in block.split("\n")]
    return ParentNode("ol", lines)

def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[1:].strip()
    raise Exception("no MD heading found")
