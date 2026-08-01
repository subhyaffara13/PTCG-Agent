
def normalize_qualifiers(
    qualifiers: AnyStr | dict[str, str] | None, encode: Literal[True] = ...
) -> str | None: ...


def normalize_qualifiers(
    qualifiers: AnyStr | dict[str, str] | None, encode: Literal[False] | None
) -> dict[str, str]: ...


def normalize_qualifiers(
    qualifiers: AnyStr | dict[str, str] | None, encode: bool | None = ...
) -> str | dict[str, str] | None: ...


def normalize_qualifiers(
    qualifiers: AnyStr | dict[str, str] | None, encode: bool | None = True
) -> str | dict[str, str] | None:
    """
    Return normalized `qualifiers` as a mapping (or as a string if `encode` is
    True). The `qualifiers` arg is either a mapping or a string.
    Always return a mapping if decode is True (and never None).
    Raise ValueError on errors.
    """
    if not qualifiers:
        return None if encode else {}

    if isinstance(qualifiers, basestring):
        qualifiers_str = qualifiers if isinstance(qualifiers, str) else qualifiers.decode("utf-8")

        # decode string to list of tuples
        qualifiers_list = qualifiers_str.split("&")
        if any("=" not in kv for kv in qualifiers_list):
            raise ValueError(
                f"Invalid qualifier. Must be a string of key=value pairs:{qualifiers_list!r}"
            )
        qualifiers_parts = [kv.partition("=") for kv in qualifiers_list]
        qualifiers_pairs: Iterable[tuple[str, str]] = [(k, v) for k, _, v in qualifiers_parts]
    elif isinstance(qualifiers, dict):
        qualifiers_pairs = qualifiers.items()
    else:
        raise ValueError(f"Invalid qualifier. Must be a string or dict:{qualifiers!r}")

    quoter = get_quoter(encode)
    qualifiers_map = {
        k.strip().lower(): quoter(v)
        for k, v in qualifiers_pairs
        if k and k.strip() and v and v.strip()
    }

    valid_chars = string.ascii_letters + string.digits + ".-_"
    for key in qualifiers_map:
        if not key:
            raise ValueError("A qualifier key cannot be empty")

        if "%" in key:
            raise ValueError(f"A qualifier key cannot be percent encoded: {key!r}")

        if " " in key:
            raise ValueError(f"A qualifier key cannot contain spaces: {key!r}")

        if any(c not in valid_chars for c in key):
            raise ValueError(
                f"A qualifier key must be composed only of ASCII letters and numbers"
                f"period, dash and underscore: {key!r}"
            )

        if key[0] in string.digits:
            raise ValueError(f"A qualifier key cannot start with a number: {key!r}")

    qualifiers_map = dict(sorted(qualifiers_map.items()))

    if not encode:
        return qualifiers_map
    return _qualifier_map_to_string(qualifiers_map) or None

