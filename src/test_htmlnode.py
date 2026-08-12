import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

prop = {}
prop["href"]="www.google.sk"
prop["alt"]="nieco"


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node1 = HTMLNode("a", "name in text", None, prop)
        node2 = HTMLNode("a", "name in text", None, prop)
        self.assertEqual(node1, node2)

    def test_eq_props(self):
        node1 = HTMLNode("a", "name in text", None, prop)
        node2 = HTMLNode("a", "name in text", None, prop)
        print('\n'+node1.props_to_html()+'\n'+node2.props_to_html())
        self.assertEqual(node1.props_to_html(), node2.props_to_html())

    def test_tag(self):
        node1 = HTMLNode("a", "text in link", None, prop)
        node2 = HTMLNode("p", "text in <P>")
        print(f"\n{node1}\n{node2}")
        self.assertNotEqual(node1, node2)

    def test_link(self):
        node = HTMLNode("a", "text on page", None, prop)
        print(f"\n{node}")
        self.assertEqual(str(node.tag)[:1], "a")

    def test_diffurl(self):
        node1 = HTMLNode("a", "text on page", props=prop)
        node2 = HTMLNode("a", "text on page", props=prop)
        if node1.props and node2.props:
            self.assertEqual(node1.props["href"], node2.props["href"])

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        print(f"\n{parent_node.to_html()}")
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")


    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        print(f"\n{parent_node.to_html()}")
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

if __name__ == "__main__":
    unittest.main()
