
def _kind_name(dtype):
    try:
        return _kind_to_stem[dtype.kind]
    except KeyError as e:
        raise RuntimeError(
            f"internal dtype error, unknown kind {dtype.kind!r}"
        ) from None

