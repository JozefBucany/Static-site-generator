
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        xxx = ""
        if self.props is not None and self.props != "":
            for item in self.props:
                xxx += f' {item}="{self.props[item]}"'
        return xxx

    def __eq__(self, other):
        return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props

    def __repr__(self):
       return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def __eq__(self, other):
        return self.tag == other.tag and self.value == other.value and self.props == other.props

    def __repr__(self):
       return f"HTMLNode({self.tag}, {self.value}, {self.props})"

    def to_html(self):
        if self.value is None:
            raise ValueError("No value present")

        if self.tag is None:
            result = self.value
        else:
            if self.props is None:
                result = "<"+self.tag+">"
            else: result = "<"+self.tag+self.props_to_html()+">"
            result += self.value
            if self.tag != "img":
                result += f"</{self.tag}>"



        return result

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def __eq__(self, other):
        return self.tag == other.tag and self.children == other.children and self.props == other.props

    def __repr__(self):
       return f"HTMLNode({self.tag}, {self.children}, {self.props})"

    def to_html(self):
        if self.tag is None:
            raise ValueError("no tag present!")

        if self.children is None:
            raise ValueError("no children specified!")

        if self.props is None:
            result = "<"+self.tag+">"
        else: result = "<"+self.tag+self.props_to_html()+">"
        for child in self.children:
            result += child.to_html()
        result += f"</{self.tag}>"

        return result
