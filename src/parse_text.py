import re

from textnode import TextType, TextNode



def split_nodes_delimiter(old_nodes, delimiter, text_type): # old_nodes = list of to do nodes
    new_nodes = []
    for old in old_nodes:
        if old.text_type != TextType.TEXT:
            new_nodes.append(old)
        if not old.text.count(delimiter)%2 == 0:
            raise Exception("uneaven occurences of Dilimiter. Every opener needs one Closer")
        new_texts = old.text.split(delimiter)

        for i in range(len(new_texts)):
            if new_texts[i] == "":
                continue
            if i%2 == 0:
                new_nodes.append(TextNode(new_texts[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(new_texts[i], text_type))
    return new_nodes

def split_nodes_image(old_nodes): # old_nodes = list of to do nodes

    new_nodes = []
    for old in old_nodes:
        images = extract_markdown_images(old.text)
        if images == []:
            new_nodes.append(old)
            continue
        text_pieces = re.split(r"!\[[^\[\]]*\]\([^\(\)]*\)" , old.text)
        for i in range( len(text_pieces) + len(images) ):
            if i%2 == 0:
                index = int(i/2)
                if text_pieces[index] == "":
                    continue
                new_nodes.append(TextNode(text_pieces[index], TextType.TEXT))
            else:
                index = int((i-1)/2)
                new_nodes.append(TextNode(images[index][0], TextType.IMAGE, images[index][1]))
    return new_nodes

def split_nodes_link(old_nodes): # old_nodes == list of to do TextNodes
    new_nodes = []
    for old in old_nodes:
        links = extract_markdown_links(old.text)
        if links == []:
            new_nodes.append(old)
            continue
        text_pieces = re.split(r"\[[^\[\]]*\]\([^\(\)]*\)" , old.text)
        for i in range( len(text_pieces) + len(links) ):
            if i%2 == 0:
                index = int(i/2)
                if text_pieces[index] == "":
                    continue
                new_nodes.append(TextNode(text_pieces[index], TextType.TEXT))
            else:
                index = int((i-1)/2)
                new_nodes.append(TextNode(links[index][0], TextType.LINK, links[index][1]))
    return new_nodes



def extract_markdown_images(text):
    images = re.findall( r"!\[([^\[\]]*)\]\(([^\(\)]*)\)" ,text)
    return images

def extract_markdown_links(text):
    links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return links

