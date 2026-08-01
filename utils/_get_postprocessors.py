
def _get_postprocessors(clsname, arg_type):
    # Since only Add, Mul, Pow can be clsname, this cache
    # is not quadratic.
    postprocessors = set()
    mappings = _get_postprocessors_for_type(arg_type)
    for mapping in mappings:
        f = mapping.get(clsname, None)
        if f is not None:
            postprocessors.update(f)
    return postprocessors

