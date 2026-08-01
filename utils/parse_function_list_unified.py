
def parse_function_list_unified(response, **options):
    """FUNCTION LIST → unified ``list[dict]`` with bytes keys.

    Accepts either RESP2 wire (``list[list]`` of flat ``[k, v, k, v, …]``
    pairs, with the nested ``b"functions"`` value also a flat list of
    flat lists) or RESP3 wire (``list[dict]`` already in nested-map
    form). Both are normalised to ``list[dict]``.
    """
    if response is None:
        return None
    result = []
    for lib in response:
        if isinstance(lib, dict):
            result.append(lib)
            continue
        lib_dict = pairs_to_dict(lib)
        func_key = b"functions" if b"functions" in lib_dict else "functions"
        if func_key in lib_dict:
            functions = lib_dict[func_key]
            lib_dict[func_key] = [
                func if isinstance(func, dict) else pairs_to_dict(func)
                for func in functions
            ]
        result.append(lib_dict)
    return result

