from textnode import TextType, TextNode
def split_nodes_delimiter(old_nodes, delimiter, text_type):
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



