class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag  # str HTML Tag name
        self.value = value  # str HTML Tag value
        self.children = children # list of HTMLNode children
        self.props = props  # dict of HTML atributes
        
    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        text = ""
        if not self.props:
            return text
        for key in self.props.keys():
            text += f" {key}=\"{self.props[key]}\""
        return text
    
    def __repr__(self):
        return f"tag=\"{self.tag}\" value=\"{self.value}\" children={self.children} props={self.props}"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("LeafNode has no value but must have a value")
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"tag=\"{self.tag}\" value=\"{self.value}\" props={self.props}"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("no tag set, tag must be set")
        if not self.children:
            raise ValueError("no children set, parent node must have children")

        html = ""
        html += f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            html += child.to_html()
        html += f"</{self.tag}>"
        return html

    def __repr__(self):
        return f"tag=\"{self.tag}\" value=\"{self.value}\" children={self.children} props={self.props}"
