
def remove_trailing_space(code: str) -> str:
    return "\n".join([line.rstrip() for line in code.split("\n")])

