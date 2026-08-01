
def is_true_slices(line: abc.Iterable) -> abc.Generator[bool, None, None]:
    """
    Find non-trivial slices in "line": yields a bool.
    """
    for k in line:
        yield isinstance(k, slice) and not is_null_slice(k)

