
def next_instruction_is_function_or_class(lines):
    """Is the first non-empty, non-commented line of the cell either a function or a class?"""
    parser = StringParser("python")
    for i, line in enumerate(lines):
        if parser.is_quoted():
            parser.read_line(line)
            continue
        parser.read_line(line)
        if not line.strip():  # empty line
            if i > 0 and not lines[i - 1].strip():
                return False
            continue
        if line.startswith("def ") or line.startswith("async ") or line.startswith("class "):
            return True
        if line.startswith(("#", "@", " ", ")")):
            continue
        return False

    return False

