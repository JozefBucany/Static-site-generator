from textnode import TextNode, TextType


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
