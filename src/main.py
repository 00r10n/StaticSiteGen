import os
import shutil
from textnode import TextNode, TextType
from htmlnode import ParentNode, LeafNode
def main():
    filecopy("./static", "./public")

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

























main()

