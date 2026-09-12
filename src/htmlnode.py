
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
        props = ""
        if self.props == "" or self.props == None:
            return props
        for prop in self.props:
            props += f' {prop}="{self.props[prop]}"'
        return props

    def __repr__(self) -> str:
        return f"Tag: {self.tag}, Value: {self.value}, Children: {self.children}, Props: {self.props}"
