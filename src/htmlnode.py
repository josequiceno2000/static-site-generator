class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None:
            return ""
        dict_to_string = lambda dictionary: "".join([f' {key}="{value}"' for key, value in dictionary.items()])
        return dict_to_string(self.props)
    
    def __eq__(self, other_node):
        return self.tag == other_node.tag and self.value == other_node.value and self.children == other_node.children and self.props == other_node.props

    def __repr__(self):
        return f"HTMLNode\nTag: {self.tag}\nValue: {self.value}\nChildren: {self.children}\nProps: {self.props}"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if not self.value:
            raise ValueError("All leaf nodes must have a value")
        elif self.tag == None:
            return self.value
        else:
            tags = self.props_to_html()
            return f"<{self.tag}{tags}>{self.value}</{self.tag}>"

    def props_to_html(self):
        return super().props_to_html()
    
    def __eq__(self, other_node):
        return super().__eq__(other_node)
    
    def __repr__(self):
        return super().__repr__()
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("every parent node needs a tag")
        if not self.children:
            raise ValueError("parent nodes must have children")
        else:
            opening = f"<{self.tag}>"
            closing = f"</{self.tag}>"
            children_html = ""
            for child in self.children:
                children_html += child.to_html()
            
            return opening + children_html + closing
