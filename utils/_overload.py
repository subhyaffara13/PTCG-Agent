
def _overload(func):
    _check_overload_body(func)
    qual_name = _qualified_name(func)
    global _overloaded_fns
    fn_overload_list = _overloaded_fns.get(qual_name)
    if fn_overload_list is None:
        fn_overload_list = []
        _overloaded_fns[qual_name] = fn_overload_list
    fn_overload_list.append(func)
    return func

