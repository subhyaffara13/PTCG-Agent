
def _create_cell(contents=None):
    if contents is not _CELL_EMPTY:
        value = contents
    return (lambda: value).__closure__[0]

