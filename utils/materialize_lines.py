
def materialize_lines(lines: list[str], indentation: int) -> str:
    output = ""
    new_line_with_indent = "\n" + " " * indentation
    for i, line in enumerate(lines):
        if i != 0:
            output += new_line_with_indent
        output += line.replace("\n", new_line_with_indent)
    return output

