import os
import shutil
from textnode import TextNode, TextType
from htmlnode import ParentNode, LeafNode
from parsemarkdown import markdown_to_html_node, extract_title
def main():
    filecopy("./static", "./public")
    generate_page("content/index.md", "template.html" , "public/index.html")
    
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

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as inp_file:
        raw_md = inp_file.read()
    with open(template_path) as template_file:
        template = template_file.read()
    htmlnodes = markdown_to_html_node(raw_md)
    html_text = htmlnodes.to_html()
    title = LeafNode("h1", extract_title(raw_md)).to_html()
    html_site = template.replace("{{ Title }}", title).replace("{{ Content }}", html_text)
    if not os.path.isdir(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
    with open(dest_path, "w") as htmlfile:
        htmlfile.write(html_site)

main()
