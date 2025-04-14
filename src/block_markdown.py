from enum import Enum
import re

from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import ParentNode, LeafNode

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown:str) -> list:
    return [block.strip() for block in markdown.split("\n\n") if block.strip()]

def block_to_block_type(block:str) -> BlockType:
    mapping = {
        BlockType.HEADING: lambda s: re.match(r"^\#{1,6}\s.+", s),
        BlockType.CODE: lambda s: re.match(r"^(?:`{3})[\s\S]+(?:`{3})$", s),
        BlockType.QUOTE: lambda s: re.match(r"(?:^>.*\n)+", s, flags=re.MULTILINE),
        BlockType.UNORDERED_LIST: lambda s: re.match(r"(^-\s.+\n)+", s, flags=re.MULTILINE),
        BlockType.ORDERED_LIST: lambda s: all(re.match(fr'^{i+1}\.\s.+', x) for i, x in enumerate(s.split('\n')))
    }
    for key, value in mapping.items():
        if value(block):
            return key
    return BlockType.PARAGRAPH

def text_to_children(text) -> list[LeafNode]:
    return list(map(lambda t: text_node_to_html_node(t),text_to_textnodes(text)))

def markdown_to_html_node(markdown:str):
    new_node = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            flat_text = block.replace('\n',' ').lstrip()
            new_node.append(ParentNode('p', text_to_children(flat_text)))
        elif block_type == BlockType.HEADING:
            split_block = block.split(' ', maxsplit=1)
            level = len(split_block[0])
            new_node.append(ParentNode(f'h{level}', text_to_children(split_block[1])))
        elif block_type == BlockType.CODE:
            leaf = text_node_to_html_node(TextNode(block.replace('```','').lstrip(), TextType.CODE))
            new_node.append(ParentNode('pre', [leaf]))
        elif block_type == BlockType.QUOTE:
            split_block = block.replace('>','').replace('\n','').lstrip()
            new_node.append(ParentNode('blockquote', text_to_children(split_block)))
        elif block_type == BlockType.UNORDERED_LIST:
            child_list = []
            for line in block.split('\n'):
                child_list.append(ParentNode('li', text_to_children(line.lstrip('-').lstrip())))
            new_node.append(ParentNode('ul', child_list))
        elif block_type == BlockType.ORDERED_LIST:
            child_list = []
            for line in block.split('\n'):
                child_list.append(ParentNode('li', text_to_children(line.split('.', maxsplit=1)[1].lstrip())))
            new_node.append(ParentNode('ol', child_list))
    return ParentNode('div', new_node)           

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith('# '):
            return block.lstrip('# ')
    raise Exception("There is no h1 heading in the markdown")




