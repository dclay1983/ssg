from textnode import TextNode, TextType
from htmlnode import LeafNode
import re


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
            if len(node_text[0]) != 0:
                new_nodes.append(
                    TextNode(text=node_text[0], text_type=TextType.TEXT))
            new_nodes.append(TextNode(text=node_text[1], text_type=text_type))
            node_text = node_text[2]
        if node_text != "":
            new_nodes.append(TextNode(node_text, TextType.TEXT))
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([\w\s]*)\]\((\S+)\)", text)


def extract_markdown_links(text):
    return re.findall(
        r"!{0}\[([\w\s\"\.\<]*)\]\((\S+)\)", text)


def split_nodes_images(old_nodes):
    new_nodes = []
    if len(old_nodes) == 0:
        raise ValueError("old_nodes is an empty list")
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        node_text = node.text
        img_matches = extract_markdown_images(node_text)
        if len(img_matches) == 0:
            new_nodes.append(node)
            continue
        for img in img_matches:
            img_alt, img_link = img
            delim = f"![{img_alt}]({img_link})"
            node_text = node_text.split(delim, 1)
            if len(node_text[0]) != 0:
                new_nodes.append(TextNode(node_text[0], TextType.TEXT))
            new_nodes.append(TextNode(img_alt, TextType.IMAGE, img_link))
            node_text = node_text[1]
        if len(node_text) != 0:
            new_nodes.append(TextNode(node_text, TextType.TEXT))
    return new_nodes


def split_nodes_links(old_nodes):
    new_nodes = []
    if len(old_nodes) == 0:
        raise ValueError("old_nodes is an empty list")
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        node_text = node.text
        lnk_matches = extract_markdown_links(node_text)
        if len(lnk_matches) == 0:
            new_nodes.append(node)
            continue
        for lnk in lnk_matches:
            lnk_alt, lnk_link = lnk
            delim = f"[{lnk_alt}]({lnk_link})"
            node_text = node_text.split(delim, 1)
            if len(node_text[0]) != 0:
                new_nodes.append(TextNode(node_text[0], TextType.TEXT))
            new_nodes.append(TextNode(lnk_alt, TextType.LINK, lnk_link))
            node_text = node_text[1]
        if len(node_text) != 0:
            new_nodes.append(TextNode(node_text, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_images(nodes)
    nodes = split_nodes_links(nodes)
    if len(nodes):
        nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    if len(nodes):
        nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    if len(nodes):
        nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    if len(nodes) == 0:
        nodes = [TextNode(text, TextType.TEXT)]
    return nodes
