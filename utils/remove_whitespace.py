
def remove_whitespace(content: str, line_separator: str = "\n") -> str:
    content = (
        content.replace(line_separator, "").replace(" ", "").replace("\t", "").replace("\f", "")
    )
    return content

