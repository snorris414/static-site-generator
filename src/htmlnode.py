class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Not implemented. To be overridden by child classes")

    def props_to_html(self):
        if self.props is None or len(self.props) == 0:
            return ""
        html = ""
        for key, val in self.props.items():
            html += f' {key}="{val}"'
        return html

    def __repr__(self):
        return f"tag: {self.tag}, value: {self.value}, children: {self.children}, props: {self.props}"
