
def _nativestr_dict(d):
    """Apply ``nativestr`` to every key and string-typed value of ``d``.

    Used by the RESP3-to-RESP2-legacy adapters so labels coming from a
    RESP3 native map match today's RESP2 ``list_to_dict`` semantics.
    """
    return {
        nativestr(k): nativestr(v) if isinstance(v, (bytes, str)) else v
        for k, v in d.items()
    }

