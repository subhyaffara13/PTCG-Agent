
def remove_color_code(s: str) -> str:
    return re.sub("\\x1b.*?m", "", s)  # this works!

