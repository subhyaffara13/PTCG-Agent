
def is_cusparse_file(rel_filepath):
    _deprecated("is_cusparse_file")
    if is_pytorch_file(rel_filepath):
        return "sparse" in rel_filepath.lower()
    return False

