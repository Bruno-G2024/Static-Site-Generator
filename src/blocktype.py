import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

def block_to_block_type(mdblock: str) -> BlockType:
    lines = mdblock.split('\n')

    if mdblock.startswith(('#', '##', '###', '####', '#####', '######')):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith('```') and lines[-1].endswith('```'):
        return BlockType.CODE
    if mdblock.startswith('>'):
        for line in lines:
            if not line.startswith('>'):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if mdblock.startswith('- '):
        for line in lines:
            if not line.startswith('- '):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if mdblock.startswith('1. '):
        i = 1
        for line in lines:
            if not line.startswith(f'{i}. '):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.UNORDERED_LIST
    
    return BlockType.PARAGRAPH

block = 'This is a new heading block\n> skdvnsod'

print(block_to_block_type(block))