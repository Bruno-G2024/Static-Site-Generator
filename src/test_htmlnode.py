import unittest
from htmlnode import HTMLNode,LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_def_param(self):
        node = HTMLNode
        self.assertTrue(node)

    def test_with_param(self):
        new_prop = {
                "href": "https://www.google.com",
                "target": "_blank",
        }
        
        node = HTMLNode
        self.assertTrue(node("p", "This is a test", props=new_prop))

    def test_props_to_html(self):
        new_prop = {
                        "href": "https://www.google.com",
                        "target": "_blank",
        }

        formated_string = ' href="https://www.google.com" target="_blank"'
        node = HTMLNode
        node3 = HTMLNode
        self.assertEqual(node().props_to_html(), "")
        self.assertEqual(node3(props=new_prop).props_to_html(), formated_string)

    def test_leaf_to_html_p(self):
        new_prop = {
                    "href": "https://www.google.com",
                    "target": "_blank",
        }
        new_url = {
                    "src": "url/of/image.jpg",
                    "alt": "_blank",
        }
        node = LeafNode("p", "Hello, world!")
        node2 = LeafNode("b", "Hello, world!")
        node3 = LeafNode("i", "Hello, world!")
        node4 = LeafNode("a", "link", new_prop)

        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        self.assertEqual(node2.to_html(), "<b>Hello, world!</b>")
        self.assertEqual(node3.to_html(), "<i>Hello, world!</i>")
        self.assertEqual(node4.to_html(), '<a href="https://www.google.com" target="_blank">link</a>')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
    )

if __name__ == "__main__":
    unittest.main()