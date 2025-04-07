from parentnode import ParentNode
from leafnode import LeafNode
import unittest


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        cnode = LeafNode("span", "child")
        pnode = ParentNode("div", [cnode])
        self.assertEqual(pnode.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        gnode = LeafNode("b", "grandchild")
        cnode = ParentNode("span", [gnode])
        pnode = ParentNode("div", [cnode])
        expected = "<div><span><b>grandchild</b></span></div>"
        self.assertEqual(pnode.to_html(), expected)

    def test_no_children_to_html(self):
        node = ParentNode("div", None)
        self.assertRaises(ValueError, node.to_html)

    def test_no_tag_to_html(self):
        cnode = LeafNode("i", "I won't work")
        node = ParentNode(None, [cnode])
        self.assertRaises(ValueError, node.to_html)


if __name__ == "__main__":
    unittest.main()
