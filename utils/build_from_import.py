
def build_from_import(fromname: str, names: list[str]) -> nodes.ImportFrom:
    """create and initialize an astroid ImportFrom import statement"""
    return nodes.ImportFrom(fromname, [(name, None) for name in names])

