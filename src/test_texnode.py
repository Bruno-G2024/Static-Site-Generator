import unittest
from textnode import TextNode, TextType, text_node_to_html_node


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

if __name__ == "__main__":
    unittest.main()