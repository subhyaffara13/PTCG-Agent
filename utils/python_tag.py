import sys

def python_tag() -> str:
    return f"py{sys.version_info.major}"


def python_tag() -> str:
    return f"py{sys.version_info[0]}"

