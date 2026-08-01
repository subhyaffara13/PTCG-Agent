
def _tuple_postprocess(res, to_unpack):
    # Unpacks a potentially nested tuple of Tensors
    # to_unpack should be a single boolean or a tuple of two booleans.
    # It is used to:
    # - invert _as_tuple when res should match the inp given to _as_tuple
    # - optionally remove nesting of two tuples created by multiple calls to _as_tuple
    if isinstance(to_unpack, tuple):
        if len(to_unpack) != 2:
            raise AssertionError("Expected to_unpack tuple to have exactly 2 elements")
        if not to_unpack[1]:
            res = tuple(el[0] for el in res)
        if not to_unpack[0]:
            res = res[0]
    else:
        if not to_unpack:
            res = res[0]
    return res

