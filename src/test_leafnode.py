import unittest
from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello World!")
        self.assertEqual(node.to_html(), "<p>Hello World!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click Me!", {"href": "google.com"})
        self.assertEqual(
            node.to_html(), "<a href=\"google.com\">Click Me!</a>")

    def test_no_value(self):
        node = LeafNode(None, None)
        self.assertRaises(ValueError, node.to_html)

    def test_no_tag(self):
        node = LeafNode(None, "This works!")
        self.assertEqual(node.to_html(), "This works!")


if __name__ == "__main__":
    unittest.main()
