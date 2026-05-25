from file_cp import file_cp
from generate_page import generate_page


def main():
    source_dir = "static"
    dest_dir = "public"

    file_cp(source_dir, dest_dir)

    generate_page("content/index.md", "template.html", "public")


main()
