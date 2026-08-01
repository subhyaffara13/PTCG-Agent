
def cpp_string(s: str) -> str:
    """Convert a python string into a c++ string literal"""
    s = s.replace("\\", "\\\\")
    s = s.replace('"', '\\"')
    s = s.replace("\a", "\\a")
    s = s.replace("\b", "\\b")
    s = s.replace("\f", "\\f")
    s = s.replace("\n", "\\n")
    s = s.replace("\v", "\\v")
    s = s.replace("\t", "\\t")
    return f'"{s}"'

