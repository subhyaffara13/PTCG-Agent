
def cell_source(cell):
    """Return the source of the current cell, as an array of lines"""
    source = cell.source
    if source == "":
        return [""]
    if source.endswith("\n"):
        return source.splitlines() + [""]
    return source.splitlines()

