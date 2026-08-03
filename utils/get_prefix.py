import os

def get_prefix(prefix_root: str, prefix_dir: str, prefix_file_name: str) -> str:
    if prefix_root:
        return f"{prefix_root}//{prefix_dir}/{prefix_file_name}"
    if not prefix_dir and not prefix_file_name:
        return ""
    return f"{prefix_dir}/{prefix_file_name}"


def get_prefix(file_read: str, name: str) -> str:
    if is_toml(file_read):
        module_name_str = 'module = "%s"' % "-".join(name.split("-")[1:])
    else:
        module_name_str = name

    return f"{file_read}: [{module_name_str}]:"


def get_prefix(fullname: str) -> str:
    """Drop the final component of a qualified name (e.g. ('x.y' -> 'x')."""
    return fullname.rsplit(".", 1)[0]


def get_prefix(module):
    p = os.path.dirname(os.path.dirname(module.__file__))
    return p

