
def parse_function_list_resp3_to_resp2_legacy(response, **options):
    """RESP3-wire FUNCTION LIST → today's RESP2 ``list[list]`` shape.

    Each library and each nested function arrives as a ``dict``; flatten
    them back to interleaved ``[k, v, k, v, …]`` lists so the Python
    shape matches what RESP2 wire produces natively.
    """
    if response is None:
        return None
    result = []
    for lib in response:
        if not isinstance(lib, dict):
            result.append(lib)
            continue
        flat = []
        for key, value in lib.items():
            flat.append(key)
            if key == b"functions" or key == "functions":
                flat.append(
                    [
                        [item for kv in func.items() for item in kv]
                        if isinstance(func, dict)
                        else func
                        for func in value
                    ]
                )
            else:
                flat.append(value)
        result.append(flat)
    return result

