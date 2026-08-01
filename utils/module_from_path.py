
def module_from_path(path: str) -> str:
    path = re.sub(r"\.pyi?$", "", path)
    # We can have a mix of Unix-style and Windows-style separators.
    parts = re.split(r"[/\\]", path)
    del parts[0]
    module = ".".join(parts)
    module = re.sub(r"\.__init__$", "", module)
    return module

