
def write_to_zip(file_path, strip_file_path, zf, prepend_str="") -> None:
    stripped_file_path = prepend_str + remove_prefix(file_path, strip_file_dir + "/")
    path = Path(stripped_file_path)
    if path.name in DENY_LIST:
        return
    zf.write(file_path, stripped_file_path)

