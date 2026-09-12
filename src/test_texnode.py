import unittest
from textnode import TextNode, TextType


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

if __name__ == "__main__":
    unittest.main()