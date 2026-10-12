
class HTMLNode():
    def __init__(self, 
                 tag: str | None = None, 
                 value: str | None = None, 
                 children: list["HTMLNode"] | None = None, 
                 props: dict[str, str] | None = None
                 ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        props = ''
        if self.props == "" or self.props == None:
            return props
        for prop in self.props:
            props += f' {prop}="{self.props[prop]}"'
        return props

    def __repr__(self) -> str:
        return f"Tag: {self.tag}, Value: {self.value}, Children: {self.children}, Props: {self.props}"


class LeafNode(HTMLNode):
    def __init__(self, tag: str | None = None, 
                 value: str | None = None, 
                 props: dict[str, str] | None = None
                 ) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            return self.value

        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

    def __repr__(self) -> str:
        return f"Tag: {self.tag}, Value: {self.value}, Props: {self.props}"


class ParentNode(HTMLNode):
    def __init__(self, tag: str, 
                 children: list["HTMLNode"], 
                 props: dict[str, str] | None = None
                 ) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Parent node must have a tag")
        if self.children is None:
            raise ValueError("Parent node must have a children")
        
        result = ''
        for leaf in self.children:
            result += f'{leaf.to_html()}'
        return f'<{self.tag}{self.props_to_html()}>{result}</{self.tag}>'

    def __repr__(self) -> str:
        return f"Tag: {self.tag}, Children: {self.children}, Props: {self.props}"
    