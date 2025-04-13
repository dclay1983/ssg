from functools import reduce


class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        html = ""
        if self.props is not None:
            for prop, value in self.props.items():
                html += f" {prop}=\"{value}\""
        return html

    def __repr__(self):
        id = self.__class__.__name__
        tag = self.tag
        value = self.value
        children = None if self.children is None else reduce(
            lambda s, c: f"{s}{c},", self.children, "")
        props = self.props_to_html()
        return f"{id}(tag={tag}, value={value}, props={props}, children={children})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError(f"ParentNode: {self} must have tag")
        if self.children is None:
            raise ValueError(f"ParentNode: {self} muse have children")
        open = f"<{self.tag}{self.props_to_html()}>"
        close = f"</{self.tag}>"
        children = reduce(lambda s, c: s+c.to_html(), self.children, "")
        return open + children + close


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError(f"LeafNode: {self} missing value")
        if self.tag is None:
            return self.value
        open = f"<{self.tag}{self.props_to_html()}>"
        close = f"</{self.tag}>"
        return f"{open}{self.value}{close}"
