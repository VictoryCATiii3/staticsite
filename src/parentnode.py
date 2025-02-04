import htmlnode

class ParentNode(htmlnode.HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode must have a tag")
        if not self.children:
            raise ValueError("ParentNode must have children")
        html_out = f"<{self.tag}{super().props_to_html()}>"
        for child in self.children:
            html_out = html_out + child.to_html()
        html_out = html_out + f"</{self.tag}>"
        return html_out
