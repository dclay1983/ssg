from htmlnode import ParentNode, LeafNode
from block import BlockType, block_to_blocktype, markdown_to_blocks
from inline import text_to_textnodes, text_node_to_html_node


def text_to_children(lines, tag=None, sl=True):
    children = []
    for line in lines:
        text = ""
        if len(line) > 1:
            text = line.split(" ", 1)[1] if sl else line
        text_nodes = text_to_textnodes(text)
        html_nodes = []
        for node in text_nodes:
            html_nodes.append(text_node_to_html_node(node))
        if tag:
            p_node = ParentNode(tag, html_nodes)
            children.append(p_node)
        else:
            children.extend(html_nodes)
    return children


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_blocktype(block)
        tag = block_type.value
        text = None
        children = None
        match block_type:
            case BlockType.QUOTE:
                children = text_to_children(block.split("\n"))
            case BlockType.PARAGRAPH:
                children = text_to_children(
                    [" ".join(block.split("\n"))], sl=False)
            case BlockType.UNORDERED_LIST | BlockType.ORDERED_LIST:
                children = text_to_children(block.split("\n"), "li")
            case BlockType.HEADING:
                content = block.split(" ", 1)
                children = text_to_children([block])
                tag = tag + f"{len(content[0])}"
            case BlockType.CODE:
                text = block[4:-3]
                children = [LeafNode("code", text)]
                tag = "pre"
        node = ParentNode(tag, children) if children else LeafNode(tag, text)
        html_nodes.append(node)
    return ParentNode("div", html_nodes)


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        tag, content = line.split(" ", 1)
        if tag == "#":
            return content
    raise Exception("markdown contains no title")
