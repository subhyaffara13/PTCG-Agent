
def normalize_filename(tmp_path, param):
    # Handles two cases, where filename should
    # be a string, or a path object.
    path = tmp_path / "file"
    if param == "string":
        return str(path)
    return path

