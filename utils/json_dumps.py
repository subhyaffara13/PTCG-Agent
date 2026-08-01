
def json_dumps(obj: object, debug: bool = False) -> bytes:
    if orjson is not None:
        if debug:
            dumps_option = orjson.OPT_INDENT_2 | orjson.OPT_SORT_KEYS
        else:
            # TODO: If we don't sort keys here, testIncrementalInternalScramble fails
            # We should document exactly what is going on there
            dumps_option = orjson.OPT_SORT_KEYS

        try:
            return orjson.dumps(obj, option=dumps_option)  # type: ignore[no-any-return]
        except TypeError as e:
            if str(e) != "Integer exceeds 64-bit range":
                raise

    if debug:
        return json.dumps(obj, indent=2, sort_keys=True).encode("utf-8")
    else:
        # See above for sort_keys comment
        return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")

