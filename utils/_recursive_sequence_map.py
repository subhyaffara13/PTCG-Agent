
def _recursive_sequence_map(f, x):
    """Recursively map a function over a sequence of arbitrary depth"""
    if isinstance(x, list | tuple):
        seq_type = type(x)
        return seq_type(_recursive_sequence_map(f, xi) for xi in x)
    elif _is_sequence_like(x):
        return [_recursive_sequence_map(f, xi) for xi in x]
    else:
        return f(x)

