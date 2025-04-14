import re

from textnode import TextNode, TextType

def extract_markdown_images(text:str) -> list:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)

def extract_markdown_links(text:str) -> list:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)

def split_nodes_delimiter(old_nodes:list[TextNode], delimiter:str, text_type:TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        node_split_text = node.text.split(delimiter)
        if len(node_split_text) %2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i, split_text in enumerate(node_split_text):
            if split_text:
                new_nodes.append(TextNode(split_text, text_type if i % 2 else TextType.TEXT))
    return new_nodes

def split_nodes_image(old_nodes:list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        node_text = node.text
        image_extract = extract_markdown_images(node_text)
        if not image_extract:
            new_nodes.append(node)
            continue
        link_map = {f"![{alt}]({url})" : TextNode(alt, TextType.IMAGE, url) for alt, url in image_extract}
        pattern = "|".join([re.escape(f"![{alt}]({url})") for alt, url in image_extract])
        node_split_text = re.split(f"({pattern})", node_text)
        text_split = [text for text in node_split_text if text.strip()]
        for txt in text_split:
            new_nodes.append(link_map.get(txt, TextNode(txt, TextType.TEXT)))
    return new_nodes

def split_nodes_link(old_nodes:list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        node_text = node.text
        link_extract = extract_markdown_links(node_text)
        if not link_extract:
            new_nodes.append(node)
            continue
        link_map = {f"[{alt}]({url})" : TextNode(alt, TextType.LINK, url) for alt, url in link_extract}
        pattern = "|".join([re.escape(f"[{alt}]({url})") for alt, url in link_extract])
        node_split_text = re.split(f"({pattern})", node_text)
        text_split = [text for text in node_split_text if text.strip()]
        for txt in text_split:
            new_nodes.append(link_map.get(txt, TextNode(txt, TextType.TEXT)))
    return new_nodes

def _curried_split_nodes_delimiter(delimiter:str, texttype:TextType):
    def _sub_split_nodes_delimiter(old_nodes:list[TextNode]) -> list[TextNode]:
        return split_nodes_delimiter(old_nodes, delimiter, texttype)
    return _sub_split_nodes_delimiter

def text_to_textnodes(text) -> list[TextNode]:
    splitter_mapping = [    
        _curried_split_nodes_delimiter("**", TextType.BOLD),
        _curried_split_nodes_delimiter("_", TextType.ITALIC),
        _curried_split_nodes_delimiter("`", TextType.CODE),
        split_nodes_image,
        split_nodes_link
    ]
    nodes = [TextNode(text, TextType.TEXT)]
    for splitter in splitter_mapping:
        nodes = splitter(nodes)
    return nodes

       

        

