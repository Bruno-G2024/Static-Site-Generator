import unittest
from split_nodes import split_nodes_delimiter
from textnode import TextNode, TextType, text_node_to_html_node
from extract_md import extract_markdown_images, extract_markdown_links


class TestTextNode(unittest.TestCase):

    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is a text node", TextType.ITALIC, "https://www.youtube.com")
        node4 = TextNode("This is a text node", TextType.ITALIC, "https://www.youtube.com")
        self.assertEqual(node, node2)
        self.assertEqual(node3, node4)
        self.assertIsInstance(node, TextNode)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is a text node", TextType.ITALIC, "https://www.youtube.com")
        node4 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
        self.assertNotEqual(node3, node4)
        self.assertIsInstance(node, TextNode)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a image", TextType.IMAGE, "https://www.xdd.com")
        html_node = text_node_to_html_node(node)
        html_node2 = text_node_to_html_node(node2)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node2.tag, "img")
        self.assertEqual(html_node2.to_html(), '<img src="https://www.xdd.com" alt="This is a image"></img>')

    def test_split_nodes(self):
        to_compare = [
            TextNode("This is text with a ", TextType.TEXT, None),
            TextNode("italic block", TextType.ITALIC, None),
            TextNode(" word", TextType.TEXT, None)
        ]
        node = TextNode("**This is text with a bold block word**", TextType.BOLD)
        node2 = TextNode("This is text with a _italic block_ word", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node], "*", TextType.BOLD), [TextNode(node.text, node.text_type, None)])
        self.assertEqual(split_nodes_delimiter([node2], "_", TextType.ITALIC), to_compare)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_link(self):
            matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
            self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

if __name__ == "__main__":
    unittest.main()