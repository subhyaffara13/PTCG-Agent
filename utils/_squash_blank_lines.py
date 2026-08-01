
def _squash_blank_lines(code: str) -> str:
    lines = code.split("\n")
    result: list[str] = []
    saw_blank = False
    for line in lines:
        if line.strip() == "":
            if saw_blank:
                continue
            saw_blank = True
        else:
            saw_blank = False
        result.append(line)
    return "\n".join(result)

