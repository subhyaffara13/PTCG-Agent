
def cell_ends_with_code(lines):
    """Is the last line of the cell a line with code?"""
    if not lines:
        return False
    if not lines[-1].strip():
        return False
    if lines[-1].startswith("#"):
        return False
    return True

