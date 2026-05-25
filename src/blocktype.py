from enum import Enum
import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(markdown):
    heading_pattern = r"^#{1,6} ?[\w\s]+"
    heading_match = re.match(heading_pattern, markdown)
    if heading_match is not None:
        return BlockType.HEADING

    code_pattern = r"^```(?:\r?\n)[\s\S]*```$"
    code_match = re.match(code_pattern, markdown)
    if code_match is not None:
        return BlockType.CODE

    quote_pattern = r"^>{1} ?[^\n]*$"
    quote_matches = re.findall(quote_pattern, markdown, flags=re.MULTILINE)
    if len(markdown.splitlines()) == len(quote_matches):
        return BlockType.QUOTE

    unordered_list_pattern = r"^-{1} ?[^\n]+$"
    ul_matches = re.findall(unordered_list_pattern, markdown, flags=re.MULTILINE)
    if len(markdown.splitlines()) == len(ul_matches):
        return BlockType.UNORDERED_LIST

    ordered_list_pattern = r"^\d+\. ?[^\n]+$"
    ol_matches = re.findall(ordered_list_pattern, markdown, flags=re.MULTILINE)
    if len(markdown.splitlines()) == len(ol_matches):
        numbers = [
            int(n.removesuffix("."))
            for n in re.findall(r"^\d+\.", markdown, re.MULTILINE)
        ]
        if numbers[0] == 1:
            is_incrementing = all(
                numbers[i] == numbers[i - 1] + 1 for i in range(1, len(numbers))
            )
            if is_incrementing:
                return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
