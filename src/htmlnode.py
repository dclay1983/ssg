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
