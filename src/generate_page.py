import re
from block_to_html import markdown_to_html_node
import os
from pathlib import Path


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


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path):
    for file in os.listdir(dir_path_content):
        content_file_path = os.path.join(dir_path_content, file)
        if os.path.isfile(content_file_path):
            file_path = Path(content_file_path)
            file_contents = file_path.read_text()

            html_node = markdown_to_html_node(file_contents)
            html_str = html_node.to_html()

            title = extract_title(file_contents)

            template_file_contents = Path(template_path).read_text()
            gen_html = template_file_contents.replace("{{ Title }}", title).replace(
                "{{ Content }}", html_str
            )
            gen_html = gen_html.replace('href="/', f'href="{base_path}')
            gen_html = gen_html.replace('src="/', f'src="{base_path}')
            dest_file_path = Path(os.path.join(dest_dir_path, "index.html"))
            Path(dest_dir_path).mkdir(parents=True, exist_ok=True)
            dest_file_path.write_text(gen_html)
        else:
            generate_pages_recursive(
                os.path.join(dir_path_content, file),
                template_path,
                os.path.join(dest_dir_path, file),
                base_path,
            )
