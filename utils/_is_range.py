
def _is_range(r):
    """A range is defined as (symbol, start, end). start and end should
    be numbers.
    """
    # TODO: prange check goes here
    return (
        isinstance(r, Tuple)
        and (len(r) == 3)
        and (not isinstance(r.args[1], str)) and r.args[1].is_number
        and (not isinstance(r.args[2], str)) and r.args[2].is_number
    )

