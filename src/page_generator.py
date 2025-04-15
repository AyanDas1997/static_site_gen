import os
import shutil

from block_markdown import extract_title, markdown_to_html_node
from htmlnode import LeafNode, HTMLNode
from main import basepath

def refresh_file(dest_path):
    if os.path.exists(dest_path):
        shutil.rmtree(dest_path)
    os.mkdir(dest_path)


def copy_path(source_path, dest_path):
    for x in os.listdir(source_path):
        new_source_path = os.path.join(source_path, x)
        if os.path.isfile(new_source_path):
            shutil.copy(new_source_path, dest_path, follow_symlinks=True)
        else:
            new_dest_path = os.path.join(dest_path, x)
            if not os.path.exists(new_dest_path):
                os.mkdir(new_dest_path)
            copy_path(new_source_path,new_dest_path)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    source_file = open(from_path, 'r')
    source_markdown = source_file.read()
    template_file = open(template_path, 'r')
    template = template_file.read()
    html_string = markdown_to_html_node(source_markdown).to_html()
    title = extract_title(source_markdown)
    html = template.replace('{{ Title }}',title).replace('{{ Content }}',html_string).replace('href="/',f'href="{basepath}').replace('src="/',f'src="{basepath}')
    dest_file = open(dest_path, 'w')
    dest_file.write(html)
    source_file.close()
    template_file.close()
    dest_file.close()

def generate_page_recursively(from_path, template_path, dest_path):
    for x in os.listdir(from_path):   
        new_from_path = os.path.join(from_path, x)
        new_dest_path = os.path.join(dest_path, x.replace('.md','.html'))
        if os.path.isfile(new_from_path):
            generate_page(new_from_path,template_path, new_dest_path)
        else:
            os.makedirs(new_dest_path, exist_ok=True)
            generate_page_recursively(new_from_path, template_path, new_dest_path)