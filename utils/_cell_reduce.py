
def _cell_reduce(obj):
    """Cell (containing values of a function's free variables) reducer."""
    try:
        obj.cell_contents
    except ValueError:  # cell is empty
        return _make_empty_cell, ()
    else:
        return _make_cell, (obj.cell_contents,)

