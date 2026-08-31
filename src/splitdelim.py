from enum import Enum

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import (
    TextNode,
    TextType,
    split_nodes_image,
    split_nodes_link,
    text_node_to_html_node,
)


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ORDERED_LIST = "ordered list"
    UNORDERED_LIST = "unordered list"

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    result = []

    for item in old_nodes:
        if item.text_type != TextType.TEXT:
            result.append(item)
        else:
            found = []
            for i in range(len(item.text)):
                if item.text[i] == delimiter:
                   found.append(i)
            if len(found)%2 != 0:
                raise Exception("Invalid Markdown syntax.")  # noqa: TRY002
            else:
                strings = item.text.split(delimiter)
                for i in range (len(strings)):
                    if i%2 == 0:
                        result.append(TextNode(strings[i], TextType.TEXT))
                    else:
                        result.append(TextNode(strings[i], text_type))


    return result

def text_to_textnodes(text:str):
    xxx:list[TextNode] = []
    xxx.append(TextNode(text, TextType.TEXT))
    xxx = split_nodes_delimiter(xxx, "_", TextType.ITALIC)
    xxx = split_nodes_delimiter(xxx, "**", TextType.BOLD)
    xxx = split_nodes_delimiter(xxx, "`", TextType.CODE)
    xxx = split_nodes_image(xxx)
    xxx = split_nodes_link(xxx)
    return xxx

def markdown_to_blocks(markdown:str)->list[str]:
    splits = markdown.split("\n\n")
    splits2:list[str] = []
    for item in splits:
        item = item.strip()
        if len(item) != 0:
            splits2.append(item)
    return splits2

def block_to_block_type(block:str):
    if block[0] == "#":
        return BlockType.HEADING;
    elif block[0] == "`":
        return BlockType.CODE;
    elif block[0] == ">":
        return BlockType.QUOTE;
    elif block[0] == "-":
        return BlockType.UNORDERED_LIST
    else:
        nums = ["1","2","3","4","5","6","7","8","9","0"]
        temp = block.split(" ")[0]
        result = True
        for i in range (len(temp)-1):
            if temp[i] not in nums:
                result = False
        if result and temp[len(temp)-1] == ".":
            return BlockType.ORDERED_LIST
        return BlockType.PARAGRAPH


def markdown_to_html_node(markdown:str):
    result = ParentNode("div", [])
    x = markdown_to_blocks(markdown)
    for item in x:
        type = block_to_block_type(item)

        match(type):
            case BlockType.PARAGRAPH:
                temp = ""
                for a in item.split("\n"):
                    temp += a+" "
                temp = temp.rstrip(" ")
                xx = LeafNode("p", temp)
                xxx= []
                xx.value = text_to_textnodes(xx.value)
                for a in xx.value:
                   xxx.append(text_node_to_html_node(a))
                xx.value = ""
                for a in xxx:
                    xx.value += a.to_html()
                xx.value = xx.value.rstrip()

            case BlockType.HEADING:
                temp = ""
                for a in item.split("\n"):
                    temp += a+" "
                temp = temp.rstrip(" ")
                s = 0
                for i in range (len(item)):
                    if item[i] == "#":
                        s += 1
                    if i == 5:
                        break
                temp = f"<h{s}>" +temp[s+1:]+f"</h{s}>"
                xx = LeafNode("p", temp)
                xxx= []
                xx.value = text_to_textnodes(xx.value)
                for a in xx.value:
                   xxx.append(text_node_to_html_node(a))
                xx.value = ""
                for a in xxx:
                    xx.value += a.to_html()
                xx.value = xx.value.rstrip()

            case BlockType.CODE:
                temp = ""
                for a in item.split("\n"):
                    if a != "```":
                        if a[0] == "`" and a[len(a)-1] == "`":
                            temp += a[1:-1]
                        else:
                            temp += a
                    temp += "\n"
                temp = "<code>"+temp+"</code>"
                xx = LeafNode("pre", temp)

            case BlockType.QUOTE:
                temp = ""
                for a in item.split("\n"):
                    temp += a[2:]+" "
                temp = temp.rstrip(" ")
                temp = "<blockquote>" +temp+"</blockquote>"
                xx = LeafNode("p", temp)
                xxx= []
                xx.value = text_to_textnodes(xx.value)
                for a in xx.value:
                   xxx.append(text_node_to_html_node(a))
                xx.value = ""
                for a in xxx:
                    xx.value += a.to_html()
                xx.value = xx.value.rstrip()

            case BlockType.ORDERED_LIST:
                temp = "<ol>"
                for a in item.split("\n"):
                    temp += "<li>"+a[3:]+"</li>"
                temp = temp +"</ol>"
                xx = LeafNode("p", temp)
                xxx= []
                xx.value = text_to_textnodes(xx.value)
                for a in xx.value:
                   xxx.append(text_node_to_html_node(a))
                xx.value = ""
                for a in xxx:
                    xx.value += a.to_html()
                xx.value = xx.value.rstrip()

            case BlockType.UNORDERED_LIST:
                temp = "<ul>"
                for a in item.split("\n"):
                    temp += "<li>"+a[2:]+"</li>"
                temp = temp +"</ul>"
                xx = LeafNode("p", temp)
                xxx= []
                xx.value = text_to_textnodes(xx.value)
                for a in xx.value:
                   xxx.append(text_node_to_html_node(a))
                xx.value = ""
                for a in xxx:
                    xx.value += a.to_html()
                xx.value = xx.value.rstrip()

        result.children.append(xx)

    return result
