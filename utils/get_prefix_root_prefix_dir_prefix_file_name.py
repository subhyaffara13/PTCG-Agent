
def get_prefix_root_prefix_dir_prefix_file_name(prefix: str) -> tuple[str, str, str]:
    if "//" in prefix:
        prefix_root, prefix = prefix.rsplit("//", 1)
    else:
        prefix_root = ""
    prefix_dir, prefix_file_name = split(prefix, "/")
    return prefix_root, prefix_dir, prefix_file_name

