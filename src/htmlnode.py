class HTMLNode:
    def __init__(self, tag, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def __repr__(self):
        if self.tag is not None:
            return f"HTMLNode(tag='{self.tag}', value='{self.value}', children={self.children}, props={self.props})"
        elif self.value is not None:
            return f"HTMLNode(value='{self.value}', children={self.children}, props={self.props})"
        else:
            return f"HTMLNode(children={self.children})"

    def to_html(self):
        raise NotImplementedError("Not implemented")

    def props_to_html(self):
        testdict = self.props
        ret_string = ""
        for key, value in testdict:
            ret_string += key + value + " "
            print(ret_string)


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError
        if self.tag is None:
            return str(self.value)
        else:
            html = f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
            return html


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError
        if not self.children:
            raise ValueError("children has to be provided in a parentNode")
        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children} , {self.props})"
