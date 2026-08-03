import re

def is_mangled(name: str) -> bool:
    return bool(re.match(r"<torch_package_\d+>", name))

