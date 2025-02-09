from textnode import TextType, TextNode
from leafnode import LeafNode
from markdown_to_html import markdown_to_html_node
import re
import os
import shutil

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

def markdown_to_blocks_original(markdown):
    if type(markdown) != str:
        raise ValueError("markdown_to_blocks(markdown) requires that markdown be a string")
    split_markdown = markdown.split("\n")
    output = []
    for i, item in enumerate(split_markdown):
        split_markdown[i] = item.strip()
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
    return output

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

def copy_source_to_destination(source, destination):
    if not os.path.exists(destination):
        os.mkdir(destination)

    for item in os.listdir(source):
        source_path = os.path.join(source, item)
        destination_path = os.path.join(destination, item)

        if os.path.isfile(source_path):
            shutil.copy(source_path, destination_path)
        else:
            copy_source_to_destination(source_path, destination_path)

def clear_and_copy_source_to_destination(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
    copy_source_to_destination(source, destination)

def extract_title(markdown):
    regex_pattern = r"^#\s+(.*)"
    match = re.search(regex_pattern, markdown, re.MULTILINE)
    if match:
        return match.group(1).strip()
    raise Exception("No h1 header found")

def generate_page(from_path, template_path, dest_path):
    print(f"Geneating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as markdown_file:
        markdown = markdown_file.read()
        markdown_file.close()
    title = extract_title(markdown)
    content = markdown_to_html_node(markdown)
    #print(content.to_html())

    with open(template_path, "r") as template_file:
        html = template_file.read()
        template_file.close()

    html = html.replace("{{ Title }}", title)
    html = html.replace("{{ Content }}", content.to_html())

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w") as destination_file:
        destination_file.write(html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    #if not os.path.exists(dest_dir_path):
    #    os.mkdir(dest_dir_path)

    template_path = os.path.abspath(template_path)
    for item in os.listdir(dir_path_content):
        print(f"dir content: {os.listdir(dir_path_content)}")
        source_path = os.path.join(dir_path_content, item)
        destination_path = os.path.join(dest_dir_path, item)

        if(os.path.isfile(source_path)):
            print(f"Generating page: {source_path} : {template_path} : {destination_path}")
            generate_page(source_path, template_path, destination_path.replace(".md", ".html"))
        else:
            print(f"Calling recursive: {source_path} : {template_path} : {destination_path}")
            generate_pages_recursive(source_path, template_path, destination_path)

def main():
    print("----------MAIN----------")
    static_dir = "static"
    public_dir = "public"
    clear_and_copy_source_to_destination(static_dir, public_dir)

    markdown = "content"
    destination = "public"
    template = "template.html"
    generate_pages_recursive(markdown, template, destination)

if __name__=="__main__":
    main()

