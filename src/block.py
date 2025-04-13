from enum import Enum
import re


class BlockType(Enum):
    PARAGRAPH = "p"
    HEADING = "h"
    CODE = "code"
    QUOTE = "blockquote"
    UNORDERED_LIST = "ul"
    ORDERED_LIST = "ol"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = [block.strip() for block in blocks if len(block) > 0]
    return blocks


def is_quote(lines):
    for line in lines:
        if line[:2] != "> ":
            if len(line) == 1 and line == ">":
                continue
            return False
    return True


def is_unordered_list(lines):
    for line in lines:
        if line[:2] != "- ":
            return False
    return True


def is_ordered_list(lines):
    line_number = 1
    for line in lines:
        if line[:3] != f"{line_number}. ":
            return False
        line_number += 1
    return True


def block_to_blocktype(block):
    lines = block.split("\n")
    if re.search(r"^#{1,6}\s", block):
        return BlockType.HEADING
    if re.search(r"^`{3}(.|\n)*`{3}$", block):
        return BlockType.CODE
    if is_quote(lines):
        return BlockType.QUOTE
    if is_unordered_list(lines):
        return BlockType.UNORDERED_LIST
    if is_ordered_list(lines):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
