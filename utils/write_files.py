
def write_files(files, root_dir):
    for file, content in files.items():
        path = root_dir / file
        path.parent.mkdir(exist_ok=True, parents=True)
        path.write_text(content, encoding="utf-8")

