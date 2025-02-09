import re

from markdown_to_html_utils import markdown_to_blocks, text_to_textnodes,text_node_to_html_node
from blocks import BlockType, block_to_block_type
from textnode import TextType, TextNode
from leafnode import LeafNode
from parentnode import ParentNode

def markdown_to_html_node(markdown):
    if markdown == "":
        return LeafNode("div", "")
    blocks = []
    children = []
    #print(blocks)
    for block in markdown_to_blocks(markdown):
        block_type = block_to_block_type(block)
        #print(block_type)
        blocks.append((block, block_type))
    #print(blocks)
    for block, block_type in blocks:
        #print(f"BLOCK: {block}")
        #print(f"BLOCK TYPE: {block_type}")
        match block_type:
            case BlockType.QUOTE:
                children.append(quote_block(block))
            case BlockType.UNORDERED_LIST:
                children.append(unordered_block(block))
            case BlockType.ORDERED_LIST:
                children.append(ordered_block(block))
            case BlockType.HEADING:
                children.append(heading_block(block))
            case BlockType.CODE:
                parent = ParentNode("pre", [LeafNode("code", block[3:-3])])
                children.append(parent)
            case BlockType.PARAGRAPH:
                children.append(paragraph_block(block))
            case _:
                raise Exception(f"Unrecognized block type: {block_type}")
    return ParentNode("div", children)

def gen_html_nodes(text_nodes):
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes

def paragraph_block(block):
    text_nodes = text_to_textnodes(block)
    nodes = gen_html_nodes(text_nodes)
    return ParentNode("p", nodes)

def quote_block(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        new_lines.append(line[1:].strip())
    new_block = "\n".join(new_lines)
    text_nodes = text_to_textnodes(new_block)
    nodes = gen_html_nodes(text_nodes)
    return ParentNode("blockquote", nodes)

def unordered_block(block):
    lines = block.split("\n")
    new_lines = []
    children = []
    for line in lines:
        new_lines.append(line[2:])
    for line in new_lines:
        text_nodes = text_to_textnodes(line)
        nodes = gen_html_nodes(text_nodes)
        children.append(ParentNode("li", nodes))
    return ParentNode("ul", children)

def ordered_block(block):
    regex_pattern = r"^\d+\.\s"
    lines = block.split("\n")
    new_lines = []
    children = []
    for line in lines:
        new_lines.append(re.sub(regex_pattern, "", line))
    for line in new_lines:
        text_nodes = text_to_textnodes(line)
        nodes = gen_html_nodes(text_nodes)
        children.append(ParentNode("li", nodes))
    return ParentNode("ol", children)

def heading_block(block):
    regex_pattern = r"^(#{1,6})\s"
    count = len(re.match(regex_pattern, block).group(1))
    new_block = re.sub(regex_pattern, "", block)
    text_nodes = text_to_textnodes(new_block)
    nodes = gen_html_nodes(text_nodes)
    return ParentNode(f"h{count}", nodes)

