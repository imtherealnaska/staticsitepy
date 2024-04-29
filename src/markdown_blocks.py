from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node
import re
from typing import List

from htmlnode import ParentNode

para = "paragraph"
head = "heading"
code = "code"
quote = "quote"
ul = "unordered_list"
ol = "ordered_list"


# ['This is **bolded** paragraph', 'This is another paragraph with *italic* text and `code` here\nThis is the
# same paragraph on a new line', '* This is a list\n* with I']
def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    new_blocsk = list()
    for b in blocks:
        if b == "":
            continue
        b = b.strip()
        new_blocsk.append(b)
    return new_blocsk


def block_to_block_type(single_block_markdown):
    blocks: List[str] = markdown_to_blocks(single_block_markdown)
    for block in blocks:
        if re.findall(r"^(#+)\s(.+)$", block) is not None:
            return head
        elif block.startswith("```") and block.endswith("```"):
            return code
        elif block.startswith(">"):
            return quote
        elif check_for_ulist(block=block):
            return ul
        elif check_for_olist(text=block):
            return ol
        return para


def check_for_ulist(block):
    lines: List[str] = block.split()
    for lin in lines:
        if lin.startswith("* ") or lin.startswith("- "):
            return True
        else:
            return False


def check_for_olist(text):
    pattern = r"^\d+\.\s.*$"
    expected_number = 1

    for line in text:
        if re.match(pattern, line):
            number = int(line.split(".")[0])
            if number != expected_number:
                return False
            expected_number += 1
        else:
            return False
    return True


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == para:
        return paragraph_to_html_node(block)
    if block_type == head:
        return heading_to_html_node(block)
    if block_type == code:
        return code_to_html_node(block)
    if block_type == ol:
        return ol_to_html_node(block)
    if block_type == ul:
        return ul_to_html_node(block)
    if block_type == quote:
        return quote_to_html_node(block)
    raise ValueError("Invalid block type")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level : {level}")
    text = block[level + 1]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])


def ol_to_html_node(block):
    items = block.split("\n")
    html_elems = []
    for elem in items:
        text = elem[2:]
        children = text_to_children(text)
        html_elems.append(ParentNode("li", children))
    return ParentNode("ol", html_elems)


def ul_to_html_node(block):
    items = block.split("\n")
    html_elems = []
    for elem in items:
        text = elem[2:]
        children = text_to_children(text)
        html_elems.append(ParentNode("li", children))
    return ParentNode("ul", html_elems)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
        content = " ".join(new_lines)
        children = text_to_children(content)
        return ParentNode("blockquote", children)
