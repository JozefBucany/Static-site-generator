import re
from enum import Enum

from htmlnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    LINK = "link"
    IMAGE = "image"
    CODE = "code"

class TextNode:
    def __init__(self, text: str, type: TextType|str, url: str|None=None):
        self.text: str = text
        self.text_type: TextType = TextType(type)
        self.url: str|None = url

    def __eq__(self, other) -> bool:
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"



def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            tag = None
        case TextType.BOLD:
            tag = "b"
        case TextType.ITALIC:
            tag = "i"
        case TextType.LINK:
            tag = "a"
        case TextType.IMAGE:
            tag = "img"
        case TextType.CODE:
            tag = "code"
        case _:
            raise Exception ("Invalid type")  # noqa: TRY002

    pps = None
    match tag:
        case "a":
            pps = {}
            pps["href"] = text_node.url
            a = LeafNode(tag, text_node.text, pps)
        case "img":
            pps = {}
            pps["src"] = text_node.url
            pps["alt"] = text_node.text
            a = LeafNode(tag, "", pps)
        case "code":
            a = LeafNode(None, f"'{text_node.text}'")
        case _:
            a = LeafNode(tag, text_node.text)


    return a

def extract_markdown_images(text: str)-> list[tuple[str,str]]:
    images = re.findall(r"\!\[([^\[\]]*)\]\((.*?)\)", text)
    return images

def extract_markdown_links(text: str)-> list[tuple[str,str]]:
    links = re.findall(r"(?<!\!)\[([^\[\]]*)\]\((.*?)\)", text)
    return links
