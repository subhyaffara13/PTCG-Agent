
def get_sdist_members(sdist_path):
    with tarfile.open(sdist_path, "r:gz") as tar:
        files = [Path(f) for f in tar.getnames()]
    # remove root folder
    relative_files = ("/".join(f.parts[1:]) for f in files)
    return {f for f in relative_files if f}

