from splitdelim import split_nodes_delimiter
from textnode import TextNode, TextType

node = TextNode("This is a text and 'this is a code' inside text", TextType.TEXT)
node2 = TextNode("This text'has code' and then 'even more code'and text", TextType.TEXT)
aaa = [node, node2]

for item in split_nodes_delimiter(aaa, "'", TextType.CODE):
    print(item)

node3 = TextNode("This is a text node", TextType.TEXT)
node4 = TextNode("This is a **bold** node", TextType.TEXT)
node5 = TextNode("This is a _italic_ node", TextType.TEXT)
node6 = TextNode("This is a 'code' node", TextType.TEXT)
node7 = TextNode("This is a **mixed** 'code' node", TextType.TEXT)
node8 = TextNode("This is a **bold** and _italic_node", TextType.TEXT)
bbb = [node3, node4]
ccc = [node5, node6]
ddd = [node7, node8]

for item in split_nodes_delimiter(bbb, "**", TextType.BOLD):
    print(item)

for item in split_nodes_delimiter(ccc, "_", TextType.ITALIC):
    print(item)

xxx = split_nodes_delimiter(ddd, "_", TextType.ITALIC)
xxx = split_nodes_delimiter(xxx, "**", TextType.BOLD)
xxx = split_nodes_delimiter(xxx, "'", TextType.CODE)

for item in xxx:
    print(item)
