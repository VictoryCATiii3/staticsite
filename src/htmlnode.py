class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def to_html(self):
        raise NotImplementedError("Not Implemented")

    def props_to_html(self):
        #Should return a string that represents the HTML attributes of the node
        html_attributes = ""
        if not self.props:
            return html_attributes
        for key in self.props.keys():
            html_attributes = html_attributes +' ' + key + '="' + self.props[key] + '"'
        return html_attributes
