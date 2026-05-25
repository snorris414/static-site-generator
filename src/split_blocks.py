def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks_stripped = list(map(lambda x: x.strip(), blocks))
    blocks_no_empty = list(filter(lambda x: x != "", blocks_stripped))
    return blocks_no_empty
