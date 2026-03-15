import os
import sys
import shutil
from textnode import TextNode, TextType
from htmlnode import ParentNode, LeafNode
from parsemarkdown import markdown_to_html_node, extract_title
def main():
    if len(sys.argv)>=2:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    filecopy("./static", "./docs")
    generate_pages_recursive("content", "template.html" , "docs", basepath)
    
def filecopy(source,destination):
    if not os.path.isdir(source) or not os.path.isdir(destination):
        raise ValueError("Directory not found")

    # clean up target directory

    shutil.rmtree(destination)
    os.mkdir(destination)

    for entity in os.listdir(source):
        current = os.path.join(source, entity)
        mirror = os.path.join(destination, entity)
        if os.path.isfile(current):
            shutil.copy(current, mirror)
            print(f"Log: CP File {current} to dest {mirror}")
        elif os.path.isdir(current):
            os.mkdir(mirror)
            print(f"Log: made dir {mirror} will recurse over directory")
            filecopy(current, mirror)

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as inp_file:
        raw_md = inp_file.read()
    with open(template_path) as template_file:
        template = template_file.read()
    htmlnodes = markdown_to_html_node(raw_md)
    html_text = htmlnodes.to_html()
    title = extract_title(raw_md)

    html_site = template.replace("{{ Title }}", title).replace("{{ Content }}", html_text)
    html_site = html_site.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')
    if not os.path.isdir(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
    with open(dest_path, "w") as htmlfile:
        htmlfile.write(html_site)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for entity in os.listdir(dir_path_content):
        subj = os.path.join(dir_path_content,entity)
        if os.path.isfile(subj):
            mirror = os.path.join(dest_dir_path, f"{entity[:-3]}.html")
            generate_page(subj, template_path, mirror, basepath)
        if os.path.isdir(subj):
            mirror = os.path.join(dest_dir_path, entity)
            os.mkdir(mirror)
            generate_pages_recursive(subj, template_path, mirror, basepath)


main()
