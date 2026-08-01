
def three_backticks_or_more(lines):
    """Return a string with enough backticks to encapsulate the given code cell in Markdown
    cf. https://github.com/mwouts/jupytext/issues/712"""
    code_cell_delimiter = "```"
    for line in lines:
        if not line.startswith(code_cell_delimiter):
            continue
        for char in line[len(code_cell_delimiter) :]:
            if char != "`":
                break
            code_cell_delimiter += "`"
        code_cell_delimiter += "`"

    return code_cell_delimiter

