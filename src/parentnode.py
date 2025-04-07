from htmlnode import HTMLNode
from functools import reduce


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have tag")
        if self.children is None:
            raise ValueError("ParentNode muse have children")
        open = f"<{self.tag}{self.props_to_html()}>"
        close = f"</{self.tag}>"
        children = reduce(lambda s, c: s+c.to_html(), self.children, "")
        return open + children + close
