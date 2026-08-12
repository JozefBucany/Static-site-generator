import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_type(self):
        node1 = TextNode("Hello", TextType.BOLD)
        node2 = TextNode("World", TextType.LINK, "www.google.sk")
        print(f"\n{node1}\n{node2}")
        self.assertNotEqual(node1, node2)

    def test_url(self):
        node = TextNode("this is not a link", TextType.LINK, "ww.google.sk")
        print(f"\n{node}")
        self.assertNotEqual(str(node.url)[:4], "www.")

    def test_wrongtype(self):
        node1 = TextNode("Hello", "link", "www.zoznam.sk")
        node2 = TextNode("World", TextType.LINK, "www.google.sk")
        print(f"\n{node1}\n{node2}")
        self.assertEqual(node1.text_type, node2.text_type)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        print(f"\n{html_node.to_html()}")
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        print(f"\n{html_node.to_html()}")
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")


    def test_italic(self):
        node = TextNode("This is a italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        print(f"\n{html_node.to_html()}")
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a italic node")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "www.google.sk")
        html_node = text_node_to_html_node(node)
        print(f"\n{html_node.to_html()}")
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props, {'href':"www.google.sk"})

    def test_image(self):
        node = TextNode("This is image", TextType.IMAGE, "./image.jpg")
        html_node = text_node_to_html_node(node)
        print(f"\n{html_node.to_html()}")
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props, {'src': './image.jpg', 'alt': 'This is image'})

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        print(f"\n{html_node.to_html()}")
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "'This is a code node'")


if __name__ == "__main__":
    unittest.main()
