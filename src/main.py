import os
import shutil
from md_html import extract_title, markdown_to_html_node


STATIC_PATH = "./static/"
PUBLIC_PATH = "./public/"
CONTENT_PATH = "./content/"
TEMPLATE_PATH = "./template.html"


def copy_directory(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.mkdir(dst)
    if not os.path.exists(src):
        raise FileExistsError(f"{src} path does not exist")

    print(f"Copying from {src} to {dst}")
    with os.scandir(src) as it:
        for entry in it:
            if entry.is_file():
                shutil.copy(entry.path, dst)
                print(f"Copied {entry.name} to {dst}")
            elif entry.is_dir():
                copy_directory(entry.path, f"{dst}{entry.name}/")


def generate_page(src, tmp_file, dst):
    print(f"Generating page from {src} to {dst} using {tmp_file}")

    if not os.path.exists(src):
        raise FileExistsError(f"{src} path does not exist")

    md, template = "", ""
    with open(src, mode="r") as f:
        md = f.read()

    with open(tmp_file, mode="r") as f:
        template = f.read()

    title = extract_title(md)
    html = markdown_to_html_node(md).to_html()
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    with open(dst, 'w', encoding="utf-8") as f:
        f.write(template)


def generate_content(src, dst):
    with os.scandir(src) as it:
        for entry in it:
            if entry.is_file():
                generate_page(entry.path, TEMPLATE_PATH, f"{dst}{
                              entry.name.split(".")[0]}.html")
            elif entry.is_dir():
                new_dst = f"{dst}{entry.name}/"
                os.mkdir(new_dst)
                generate_content(entry.path, new_dst)


def main():
    copy_directory(STATIC_PATH, PUBLIC_PATH)
    generate_content(CONTENT_PATH, PUBLIC_PATH)


if __name__ == "__main__":
    main()
