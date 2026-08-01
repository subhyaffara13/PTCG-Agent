
def get_framelocals_idx(code: types.CodeType, var_name: str) -> int:
    # Refer to index in the frame's localsplus directly.
    # NOTE: name order for a code object doesn't change.
    # NOTE: we need to find the LAST matching index because <= 3.10 contains
    # duplicate names in the case of cells: a name can be both local and cell
    # and will take up 2 slots of the frame's localsplus. The correct behavior
    # is to refer to the cell, which has a higher index.
    framelocals_names_reversed = code_framelocals_names_reversed_cached(code)
    framelocals_idx = (
        len(framelocals_names_reversed) - framelocals_names_reversed.index(var_name) - 1
    )
    return framelocals_idx

