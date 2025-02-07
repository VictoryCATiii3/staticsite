from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

def block_to_block_type(block):
    if block == "":
        return BlockType.PARAGRAPH

    if block[0] == "#":
        return BlockType.HEADING
    elif block[:3] == "```" and block[-3:] == "```":
        return BlockType.CODE
    elif block[0] == ">":
        block_lines = block.split("\n")
        is_quote = True
        for line in block_lines:
            is_quote = is_quote and line[0] == ">"
        if is_quote:
            return BlockType.QUOTE
        return BlockType.PARGRAPH
    elif block[0] == "*" or block[0] == "-":
        block_lines = block.split("\n")
        is_unordered_list = True
        for line in block_lines:
            is_unordered_list = is_unordered_list and (line[0] == "*" or line[0] =="-")
        if is_unordered_list:
            return BlockType.UNORDERED_LIST
        return BlockType.PARGRAPH
    elif block[:2] == "1.":
        line_num = 1
        is_ordered_list = True
        block_lines = block.split("\n")
        for line in block_lines:
            is_ordered_list = is_ordered_list and line[:2] == f"{line_num}."
            line_num += 1
        if is_ordered_list:
            return BlockType.ORDERED_LIST
        return BlockType.PARAGRAPH
    else:
        return BlockType.PARAGRAPH
