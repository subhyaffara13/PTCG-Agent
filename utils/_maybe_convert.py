
def _maybe_convert(values: np.ndarray, val_kind: str, encoding: str, errors: str):
    assert isinstance(val_kind, str), type(val_kind)
    if _need_convert(val_kind):
        conv = _get_converter(val_kind, encoding, errors)
        values = conv(values)
    return values

