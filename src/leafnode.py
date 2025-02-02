import htmlnode

class LeafNode(htmlnode.HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("All leaf nodes must have a value")
        if not self.tag:
            return value
        return f"<{self.tag}{super().props_to_html()}>{self.value}</{self.tag}>"
