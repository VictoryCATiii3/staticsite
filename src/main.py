from textnode import TextType, TextNode
from leafnode import LeafNode
import re

print("hello world")

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

def split_nodes_images(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text
        images = extract_markdown_images(text)
        for image in images:
            split_result = text.split(f"![{image[0]}]({image[1]})")
            if split_result != "":
                new_nodes.append(TextNode(split_result[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE))
            text = split_result[-1]
        if text != "":
            new_nodes.append(TextNode(text, TextType.TEXT))

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


def main():
    text_node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    print(text_node)

    #Test split_nodes_delimiter
    link_test_text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    test_node = TextNode(link_test_text, TextType.TEXT)
    new_nodes = split_nodes_link([test_node])
    print(new_nodes)

main()
