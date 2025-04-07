from textnode import TextNode, TextType
from leafnode import LeafNode


def text_node_to_html_node(text_node):
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
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode(
                "img",
                "",
                {"src": text_node.url, "alt": text_node.text}
            )
    raise ValueError("Invalid TextType")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    if len(old_nodes) == 0:
        raise ValueError("old_nodes is an empty list")
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        node_text = node.text
        while delimiter in node_text:
            node_text = node_text.split(delimiter, 2)
            if len(node_text) < 3:
                raise Exception("invalid markdown syntax")
            if len(node_text[0]) != "":
                new_nodes.append(
                    TextNode(text=node_text[0], text_type=TextType.TEXT))
            new_nodes.append(TextNode(text=node_text[1], text_type=text_type))
            node_text = node_text[2]
        if node_text != "":
            new_nodes.append(TextNode(node_text, TextType.TEXT))
    return new_nodes
