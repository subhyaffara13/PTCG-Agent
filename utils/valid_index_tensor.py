
def valid_index_tensor(index: tuple[None | slice, ...], dims: list[DVar]) -> Constraint:
    """
    if the slice instances exceed the length of the dimensions
    then this is a type error so we return False
    """
    slice_count = 0
    for s in index:
        if isinstance(s, slice):
            slice_count += 1
    if slice_count > len(dims):
        return F()
    else:
        return T()

