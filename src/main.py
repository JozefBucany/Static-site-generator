import os
import shutil
from tempfile import template

from splitdelim import markdown_to_html_node


def copydir(srcpath:str, destpath:str):
    listdir = os.listdir(srcpath)
    for item in listdir:
        print(srcpath+"/"+item)
        if os.path.isfile(srcpath+"/"+item):
            shutil.copy(srcpath+"/"+item, destpath+"/"+item)
        if os.path.isdir(srcpath+"/"+item):
            os.mkdir(destpath+"/"+item)
            copydir(srcpath+"/"+item, destpath+"/"+item)

def copy_new(srcpath: str, target: str):
    if os.path.exists(target):
        print("removing old content...")
        shutil.rmtree(target)
    os.mkdir(target)
    copydir(srcpath, target)
    print("new content copied")

def extract_title(markdown):
    for item in markdown.split("\n"):
        if len(item)>1:
            if item[0] == "#" and item[1] != "#":
                return item[1:].strip()
    raise Exception("No h1 heading found")

def generate_page(from_path:str, template_path:str, dest_path:str):
    print(f"Generating webpage from {from_path} to {dest_path} using template from {template_path}...")
    with open (from_path) as f:
        from_file = f.read()
    with open (template_path) as f:
        template_file = f.read()
    title = extract_title(from_file)
    markd = markdown_to_html_node(from_file)
    from_file = markd.to_html()
    template_file = template_file.replace("{{ Title }}", title)
    template_file = template_file.replace("{{ Content }}", from_file)
    with open(dest_path, mode="w") as f:
        f.write(template_file)






def main():
    copy_new("./static", "./public")

    generate_page("./content/index.md", "./template.html", "./public/index.html")


main()
