
def array_shapes(draw, min_dims=1, max_dims=None, min_side=1, max_side=None, max_numel=None):
    """Return a strategy for array shapes (tuples of int >= 1)."""
    if min_dims >= 32:
        raise AssertionError(f"Expected min_dims < 32, got {min_dims}")
    if max_dims is None:
        max_dims = min(min_dims + 2, 32)
    if max_dims >= 32:
        raise AssertionError(f"Expected max_dims < 32, got {max_dims}")
    if max_side is None:
        max_side = min_side + 5
    candidate = st.lists(st.integers(min_side, max_side), min_size=min_dims, max_size=max_dims)
    if max_numel is not None:
        candidate = candidate.filter(lambda x: reduce(int.__mul__, x, 1) <= max_numel)
    return draw(candidate.map(tuple))

