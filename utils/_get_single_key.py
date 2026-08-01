
def _get_single_key(pat: str) -> str:
    keys = _select_options(pat)
    if len(keys) == 0:
        _warn_if_deprecated(pat)
        raise OptionError(f"No such keys(s): {pat!r}")
    if len(keys) > 1:
        raise OptionError("Pattern matched multiple keys")
    key = keys[0]

    _warn_if_deprecated(key)

    key = _translate_key(key)

    return key

