from converters import text_node_to_html_node, split_nodes_delimiter
from textnode import TextType, TextNode
import unittest


class TestTextToHTML(unittest.TestCase):
    def test_text_to_html(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_invalid_text_node(self):
        node = TextNode("This is invalid", "Wrong type")
        self.assertRaises(ValueError, text_node_to_html_node, node)

    def test_img_to_html(self):
        node = TextNode("Pretty sunrise", TextType.IMAGE,
                        "~/Pictures/sunrise.jpg")
        hnode = text_node_to_html_node(node)
        self.assertEqual(hnode.tag, "img")
        self.assertEqual(
            hnode.props_to_html(), " src=\"~/Pictures/sunrise.jpg\" alt=\"Pretty sunrise\"")


class TestSplitNodeDelimiter(unittest.TestCase):
    def test_split_nodes_no_inline(self):
        node = TextNode("No inline elements here", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0], node)

    def test_split_nodes_no_text(self):
        nodes = [
            TextNode("Bold", TextType.BOLD),
            TextNode("Italic", TextType.ITALIC),
            TextNode("Code", TextType.CODE)
        ]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text_type, TextType.BOLD)

    def test_split_nodes_text_w_bold(self):
        node = TextNode("The **best** part of waking up...", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)

    def test_split_nodes_multiple_elements_one_line(self):
        node = TextNode("is _Folgers_ in **your** `cup`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 6)
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[3].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[5].text_type, TextType.CODE)


if __name__ == "__main__":
    unittest.main()
