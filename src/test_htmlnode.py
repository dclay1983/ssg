import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_to_props(self):
        node = HTMLNode(props={"href": "_blank", "class": "test"})
        self.assertEqual(node.props_to_html(),
                         " href=\"_blank\" class=\"test\"")

    def test_no_props_to_props(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_print_node(self):
        node = HTMLNode()
        self.assertEqual(
            f"{node}", "HTMLNode(tag=None, value=None, props="", children=None)")


if __name__ == "__main__":
    unittest.main()
