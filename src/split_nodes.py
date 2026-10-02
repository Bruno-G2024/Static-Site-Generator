from textnode import TextNode, TextType
from extract_md import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:

    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        current = old_node.text
        extracted_image = extract_markdown_images(old_node.text)
        if extracted_image is None:
            new_nodes.append(old_node)
            continue

        for i in range(len(extracted_image)):
            markdown_syntax = f"![{extracted_image[i][0]}]({extracted_image[i][1]})"
            sections = current.split(markdown_syntax, 1)

            if len(sections) != 2:
                raise ValueError("invalid markdown, formatted section not closed")

            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(extracted_image[i][0], TextType.IMAGE, extracted_image[i][1]))
            current = sections[1]

        if current != "":
            new_nodes.append(TextNode(current, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:

    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        current = old_node.text
        extracted_links = extract_markdown_links(old_node.text)
        if extracted_links is None:
            continue

        for i in range(len(extracted_links)):
            markdown_syntax = f"[{extracted_links[i][0]}]({extracted_links[i][1]})"
            sections = current.split(markdown_syntax, 1)

            if len(sections) != 2:
                raise ValueError("invalid markdown, formatted section not closed")

            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(extracted_links[i][0], TextType.LINK, extracted_links[i][1]))
            current = sections[1]

        if current != "":
            new_nodes.append(TextNode(current, TextType.TEXT))

    return new_nodes

def text_to_textnode(text: str) -> list[TextNode]:
    node = TextNode(text, TextType.TEXT)

    bold_split = split_nodes_delimiter([node], "**", TextType.BOLD)
    italic_split = split_nodes_delimiter(bold_split, "_", TextType.ITALIC)
    code_split = split_nodes_delimiter(italic_split, "`", TextType.CODE)
    image_split = split_nodes_image(code_split)
    link_split = split_nodes_link(image_split)

    return link_split

#print(text_to_textnode("This is **text** with an _italic_ **word** and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev) and also ![anashe](https://i.imgur.com/ofkvjs.jpeg) to"))