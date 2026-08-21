import unittest

from textnode import extract_markdown_images, extract_markdown_links
from main import extract_title


class TestTextNode(unittest.TestCase):

    def test_extract_markdown_images1(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images2(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan","https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_extract_markdown_link1(self):
        matches = extract_markdown_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_link2(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube","https://www.youtube.com/@bootdotdev")], matches)

    def test_extract_title(self):
        match = extract_title("""
asdf
##  41233xcv

#    654asd67z
asdf
            """)
        self.assertEqual(match, "654asd67z")
