
def cell_has_code(lines):
    """Is there any code in this cell?"""
    for i, line in enumerate(lines):
        stripped_line = line.strip()
        if stripped_line.startswith("#"):
            continue

        # Two consecutive blank lines?
        if not stripped_line:
            if i > 0 and not lines[i - 1].strip():
                return False
            continue

        return True

    return False

