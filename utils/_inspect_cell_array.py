
def _inspect_cell_array(ndarray):
    """Construct lists from cell arrays (loaded as numpy ndarrays), recursing
    into items if they contain mat_struct objects."""
    elem_list = []
    for sub_elem in ndarray:
        if isinstance(sub_elem, mat_struct):
            elem_list.append(_matstruct_to_dict(sub_elem))
        elif _has_struct(sub_elem):
            elem_list.append(_inspect_cell_array(sub_elem))
        else:
            elem_list.append(sub_elem)
    return elem_list

