import re

def extract_markdown_images(text) -> list[tuple]:
    image_link = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

    return image_link

def extract_markdown_links(text) -> list[tuple]:
    regular_link = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

    return regular_link
