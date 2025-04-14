from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text, text_type: TextType, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
        
    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self):
        return f"TextNode(text: {self.text}, text_type: {self.text_type.value}, url: {self.url})"
    
def text_node_to_html_node(text_node:TextNode) -> LeafNode:
    if not isinstance(text_node, TextNode):
        raise ValueError("Expected a TextNode instance")
    
    mapping = {
        TextType.TEXT : lambda tn: LeafNode(value=tn.text),
        TextType.BOLD : lambda tn: LeafNode(tag='b', value=tn.text),
        TextType.ITALIC : lambda tn: LeafNode(tag='i', value=tn.text),
        TextType.CODE : lambda tn: LeafNode(tag='code', value=tn.text),
        TextType.LINK : lambda tn: LeafNode(tag='a', value=tn.text, props={"href": tn.url}),
        TextType.IMAGE : lambda tn: LeafNode(tag='img',value="", props={"src": tn.url, "alt": tn.text})
    }

    if text_node.text_type not in mapping:
        raise ValueError(f"Unsupported text type: {text_node.text_type}")
    return mapping[text_node.text_type](text_node)