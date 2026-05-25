import re
from block_to_html import markdown_to_html_node
import os


def extract_title(markdown):
    h1_regex_pattern = r"^#\s[^\n]+$"
    matches = re.findall(h1_regex_pattern, markdown, flags=re.MULTILINE)
    if matches is None or len(matches) == 0:
        raise Exception("No h1 heading found in markdown")
    if len(matches) > 1:
        raise Exception(
            "More than 1 h1 heading found in markdown. Only 1 h1 heading is permitted"
        )
    title_line = matches[0]
    title_split = title_line.split("# ")
    title = title_split[1].strip()
    return title


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    file_contents = None
    with open(from_path) as f:
        file_contents = f.read()

    template_file_contents = None
    with open(template_path) as f:
        template_file_contents = f.read()

    html_node = markdown_to_html_node(file_contents)
    html_str = html_node.to_html()

    title = extract_title(file_contents)

    gen_html = template_file_contents.replace("{{ Title }}", title).replace(
        "{{ Content }}", html_str
    )

    os.makedirs(dest_path, exist_ok=True)

    with open(os.path.join(dest_path, "index.html"), "w") as f:
        f.write(gen_html)
