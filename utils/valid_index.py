
def valid_index(index: int, dims: list[DVar]) -> Constraint:
    """
    Given a list of dimensions, checks if an index is valid in the list
    """
    try:
        dims[index]
        return T()
    except IndexError:
        return F()

