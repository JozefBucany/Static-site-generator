from locale import CODESET
from pickle import LIST

from textnode import TextNode, TextType, split_nodes_image, split_nodes_link
from enum import Enum

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
