from textnode import TextNode, TextType

def main():
    new_object = TextNode

    print(new_object("Some text to test", TextType.BOLD, "https://www.youtube.com"))


main()