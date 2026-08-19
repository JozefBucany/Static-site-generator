import unittest

from splitdelim import (
    BlockType,
    block_to_block_type,
    markdown_to_blocks,
    markdown_to_html_node,
    text_to_textnodes,
)
from textnode import (
    TextNode,
    TextType,
    split_nodes_image,
    split_nodes_link,
    text_node_to_html_node,
)


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
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
           new_nodes)

    def test_split_nodes(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT)
        a = []
        a.append(node)

        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT)
        b=[]
        b.append(node)

        x = split_nodes_image(b)
        y = split_nodes_link(a)

        for item in x:
            print(item)

        for item in y:
            print(item)

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type(self):
        md1 = "This is **bolded** paragraph"
        md2 = "#This is another paragraph with _italic_ text and `code` here"
        md3 = "```This is the same paragraph on a new line"
        md4 = "- This is another paragraph with _italic_ text and `code` here\n- This is the same paragraph on a new line"
        md5 = "9. This is another paragraph with _italic_ text and `code` here\n12. This is the same paragraph on a new line"
        md6 = "> This is **bolded** paragraph"

        blocks1 = block_to_block_type(md1)
        blocks2 = block_to_block_type(md2)
        blocks3 = block_to_block_type(md3)
        blocks4 = block_to_block_type(md4)
        blocks5 = block_to_block_type(md5)
        blocks6 = block_to_block_type(md6)

        self.assertEqual(blocks1, BlockType.PARAGRAPH)
        self.assertEqual(blocks2, BlockType.HEADING)
        self.assertEqual(blocks3, BlockType.CODE)
        self.assertEqual(blocks4, BlockType.UNORDERED_LIST)
        self.assertEqual(blocks5, BlockType.ORDERED_LIST)
        self.assertEqual(blocks6, BlockType.QUOTE)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
            )


    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
            )

if __name__ == "__main__":
    unittest.main()
