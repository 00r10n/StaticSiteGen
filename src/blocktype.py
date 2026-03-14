import re
from enum import Enum



class BlockType(Enum):
    PARAGRAPH = "PARAGRAPH"
    HEADING = "HEADING"
    CODE = "CODE"
    QUOTE = "QUOTE"
    UNORDERED_LIST = "UNORDERED_LIST"
    ORDERED_LIST = "ORDERED_LIST"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = [i.strip() for i in blocks if not i == ""]
    return blocks
    

def block_to_block_type(block):

    if re.match(r"#{1,6} ", block):
        return BlockType.HEADING
    
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    lines = block.split("\n")

    match = True
    for line in lines:
        if not line.startswith(">"):
            match = False
            break
    if match:
        return BlockType.QUOTE

    match = True
    for line in lines:
        if not line.startswith("- "):
            match = False
            break
    if match:
        return BlockType.UNORDERED_LIST

    match = True
    nr = 0
    for line in lines:
        nr += 1
        if not line.startswith(f"{nr}. "):
            match = False
            break
    if match:
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH
