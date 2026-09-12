import unittest
from htmlnode import HTMLNode


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

if __name__ == "__main__":
    unittest.main()