
def ensure_files(root_path, files):
    for file in files:
        path = root_path / file
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch()

