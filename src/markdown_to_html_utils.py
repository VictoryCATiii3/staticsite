from textnode import TextType, TextNode
from leafnode import LeafNode
import re

def markdown_to_blocks(markdown):
    if type(markdown) != str:
        raise ValueError("markdown_to_blocks(markdown) requires that markdown be a string")
    split_markdown = markdown.split("\n")
    output = []
    temp_string = ""
    for item in split_markdown:
        if item == "":
            if temp_string != "":
                output.append(temp_string)
                temp_string = ""
        else:
            if temp_string == "":
                temp_string = item
            else:
                temp_string = temp_string + "\n" + item
    if temp_string != "":
        output.append(temp_string)
    for i, item in enumerate(output):
        output[i] = item.strip()
    return output

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            count = node.text.count(delimiter)
            if count % 2 != 0:
                raise Exception("Invalid markdown syntax")
            split_node = node.text.split(delimiter)
            first_delim = node.text[0:len(delimiter)] == delimiter
            for i, part in enumerate(split_node):
                if part == "":
                    first_delim = not first_delim
                    continue
                if i % 2 != first_delim:
                    new_nodes.append(TextNode(part, text_type))
                else:
                    new_nodes.append(TextNode(part, TextType.TEXT))
    return new_nodes

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text
        images = extract_markdown_images(text)
        for image in images:
            split_result = text.split(f"![{image[0]}]({image[1]})")
            if split_result[0] != "":
                new_nodes.append(TextNode(split_result[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            text = split_result[-1]
        if text != "":
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text
        links = extract_markdown_links(text)
        for link in links:
            split_result = text.split(f"[{link[0]}]({link[1]})", 1)
            if split_result[0] != "":
                new_nodes.append(TextNode(split_result[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            text = split_result[-1]
        if text != "":
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    if type(text) != str:
        raise ValueError("text_to_textnodes(text) requires that text be a string")
    node = TextNode(text, TextType.TEXT)
    nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def text_node_to_html_node(text_node):
    #print(self.text_node.text_type)
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href":text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src":text_node.url, "alt":text_node.text})
        case _:
            raise Exception("Unrecognized TextNode.text_type")
