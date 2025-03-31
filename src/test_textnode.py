import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_link_image(self):
        n = TextNode("This is a text node", TextType.LINK)
        n2 = TextNode("This is a text node", TextType.IMAGE)
        self.assertNotEqual(n, n2)

    def test_link_no_url(self):
        n = TextNode("This is a text node", TextType.LINK, "content/there.md")
        n2 = TextNode("This is a text node", TextType.LINK, None)
        self.assertNotEqual(n, n2)


if __name__ == "__main__":
    unittest.main()
