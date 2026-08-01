
def split_concatenated_json_objects(raw: str) -> List[Dict[str, Any]]:
    """
    Split a string that contains one or more concatenated JSON objects into
    a list of parsed dicts.

    LLM providers (notably Bedrock Claude Sonnet 4.5) sometimes return
    multiple tool-call argument objects concatenated in a single
    ``arguments`` string, e.g.::

        '{"command":["curl",...]}{"command":["curl",...]}{"command":["curl",...]}'

    ``json.loads()`` fails on this with ``JSONDecodeError: Extra data``.
    This helper uses ``json.JSONDecoder.raw_decode()`` to walk the string
    and extract each JSON object individually.

    Returns
    -------
    list[dict]
        A list of parsed dicts – one per JSON object found.  If *raw* is
        empty or whitespace-only, an empty list is returned.

    Raises
    ------
    json.JSONDecodeError
        If the string contains text that cannot be parsed as JSON at all.
    """
    import json

    raw = raw.strip()
    if not raw:
        return []

    decoder = json.JSONDecoder()
    results: List[Dict[str, Any]] = []
    idx = 0
    length = len(raw)

    while idx < length:
        # Skip whitespace between objects
        while idx < length and raw[idx] in " \t\n\r":
            idx += 1
        if idx >= length:
            break

        obj, end_idx = decoder.raw_decode(raw, idx)
        if isinstance(obj, dict):
            results.append(obj)
        else:
            # Non-dict JSON value – wrap in empty dict (Bedrock requires
            # toolUse.input to be an object).
            results.append({})
        idx = end_idx

    return results

