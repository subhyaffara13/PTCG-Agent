
def convert_binary_cache_to_json(data: bytes, *, implicit_names: bool = True) -> Json:
    tree = MypyFile.read(ReadBuffer(data))
    return convert_mypy_file_to_json(tree, Config(implicit_names=implicit_names))

