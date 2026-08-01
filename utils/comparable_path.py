
def comparable_path(str_with_path: str) -> str:
    return str_with_path.lower().replace(os.sep, "/").replace("//", "/")

