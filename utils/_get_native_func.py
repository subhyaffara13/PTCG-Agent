
def _get_native_func(xp, namespace, f_name, *, alt_names_map=None):
    if alt_names_map is None:
        alt_names_map = {}
    f_name = alt_names_map.get(get_native_namespace_name(xp), f_name)
    f = getattr(namespace, f_name, None)
    if f is None and hasattr(xp, 'special'):
        # Currently dead branch, in anticipation of 'special' Array API extension
        # https://github.com/data-apis/array-api/issues/725
        f = getattr(xp.special, f_name, None)
    return f

