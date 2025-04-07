from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if not self.value:
            raise ValueError("LeafNode missing value")
        if not self.tag:
            return self.value
        open = f"<{self.tag}{self.props_to_html()}>"
        close = f"</{self.tag}>"
        return f"{open}{self.value}{close}"
