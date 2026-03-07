class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag  # str HTML Tag name
        self.value = value  # str HTML Tan value
        self.children = children # list of HTMLNode children
        self.props = props  # dict of HTML atributes
        
    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        text = ""
        for key in self.props.keys():
            text += f' {key}="{self.props[key]}"'
        return text
    
    def __repr__(self):
        return f'tag="{self.tag}" value="{self.value}" children={self.children} props={self.props}'
    
    
