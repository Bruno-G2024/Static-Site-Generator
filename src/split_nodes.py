from blocktype import block_to_block_type, BlockType
from htmlnode import ParentNode, HTMLNode, LeafNode
from textnode import TextNode, TextType, text_node_to_html_node
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

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split('\n\n')

    new_blocks = []

    for block in blocks:
        if block == '':
            continue
        new_blocks.append(block.strip())
    
    return new_blocks 

def tag_block(blocktype: BlockType, block: str) -> str:
    if blocktype not in BlockType:
        raise ValueError("The type value is not valid for a BlockType Value")
    if blocktype == BlockType.HEADING:
        starwith = '#'
        for i in range(1, 7):
            if block.startswith(starwith):
                starwith += '#'
                continue
            return f'h{i - 1}'
    elif blocktype == BlockType.CODE:
        return 'pre'
    elif blocktype == BlockType.QUOTE:
        return 'blockquote'
    elif blocktype == BlockType.UNORDERED_LIST:
        return 'ul'
    elif blocktype == BlockType.ORDERED_LIST:
        return 'ol'
    return 'p'

def text_to_children(text: str) -> list[HTMLNode]:
    leaf_nodes = []
    new_text_nodes = text_to_textnode(text.strip('#> '))
    for text_node in new_text_nodes:
        leaf_nodes.append(text_node_to_html_node(text_node))

    return leaf_nodes

def text_to_text_code(text: str) -> LeafNode:
    text_node = TextNode(text.strip('```\n'), TextType.CODE)
    #print(text_node)
    return text_node_to_html_node(text_node)

def markdown_to_html_node(markdown) -> ParentNode:
    blocks = markdown_to_blocks(markdown)

    new_html_node = []
    for block in blocks:
        block_type = block_to_block_type(block)
        #print(block_type)
        tag = tag_block(block_type, block)
        if block_type == BlockType.CODE:
            #print(tag)
            new_html_node.append(ParentNode('pre', [text_to_text_code(block)]))
        elif block_type == BlockType.UNORDERED_LIST:
            line_list = []
            for line in block.split('\n'):
                line_list.append(ParentNode('li', text_to_children(line.removeprefix('- '))))
            new_html_node.append(ParentNode(tag, line_list))
        elif block_type == BlockType.ORDERED_LIST:
            line_list = []
            n_start = 1
            for line in block.split('\n'):
                line_list.append(ParentNode('li', text_to_children(line.removeprefix(f'{n_start}. '))))
                n_start += 1
            new_html_node.append(ParentNode(tag, line_list))
        else:
            new_html_node.append(ParentNode(tag, text_to_children(block)))
       
    return ParentNode('div', new_html_node)

md = """
## This is **bolded** paragraph
text in a p
tag here

> This is another paragraph with _italic_ text and `code` here

"""
md2 = """
This is **bolded** paragraph
text in a p
tag here
"""

md3 = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

md4 = """
This is a text with a list

- - this is the first line - with a hyphen in the midle
- this- is the second line whit a _italic_ word
- This is the third line with a **bolded** word
"""

md5 = """
This is a text with a list

1. - this is the first line - with a hyphen in the midle
2. this- is the second line whit a _italic_ word
3. This is the third line with a **bolded** word
"""
blocks = markdown_to_html_node(md5)
html = blocks.to_html()
print(html)
#print(text_to_children(md2))
#print(text_to_text_code(md3).to_html())