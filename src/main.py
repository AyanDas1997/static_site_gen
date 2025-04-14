from copy_path import copy_path, refresh_file, generate_page_recursively

default_source_path = 'static'
default_dest_path = 'public'
template_path = 'template.html'
default_from_path = 'content'

def main():
    refresh_file(default_dest_path) 
    copy_path(default_source_path, default_dest_path)
    generate_page_recursively(default_from_path, template_path, default_dest_path)

main()