
def _simplify_cells(d):
    """Convert mat objects in dict to nested dicts."""
    for key in d:
        if isinstance(d[key], mat_struct):
            d[key] = _matstruct_to_dict(d[key])
        elif _has_struct(d[key]):
            d[key] = _inspect_cell_array(d[key])
    return d

