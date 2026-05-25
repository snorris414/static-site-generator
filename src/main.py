from file_cp import file_cp
from generate_page import generate_pages_recursive
import sys


def main():
    base_path = "/"
    if len(sys.argv) > 1:
        base_path = sys.argv[1]

    source_dir = "static"
    dest_dir = "public"

    file_cp(source_dir, dest_dir)

    generate_pages_recursive("content", "template.html", "public", base_path)


main()
