import sys
import os
from page_generator import copy_path, refresh_file, generate_page_recursively

default_source_path = 'static'
default_dest_path = 'docs'
default_template_path = 'template.html'
default_from_path = 'content'

def main():
    refresh_file(default_dest_path)
    copy_path(default_source_path,default_dest_path)
    generate_page_recursively(default_from_path, default_template_path, default_dest_path)

main()