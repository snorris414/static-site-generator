from file_cp import file_cp
from generate_page import generate_pages_recursive


def main():
    source_dir = "static"
    dest_dir = "public"

    file_cp(source_dir, dest_dir)

    generate_pages_recursive("content", "template.html", "public")


main()
