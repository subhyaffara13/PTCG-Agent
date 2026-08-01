
def empty_line_normalizer(code: str) -> str:
    """
    Normalize code: remove empty lines.
    """
    normal_code = re.sub(r"[\r\n]+", "\n", code)
    return normal_code

