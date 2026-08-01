
def _unconvert_index(data, kind: str, encoding: str, errors: str) -> np.ndarray | Index:
    index: Index | np.ndarray

    if kind.startswith("datetime64"):
        if kind == "datetime64":
            # created before we stored resolution information
            index = DatetimeIndex(data, copy=False)
        else:
            index = DatetimeIndex(data.view(kind), copy=False)
    elif kind.startswith("timedelta64"):
        if kind == "timedelta64":
            # created before we stored resolution information
            index = TimedeltaIndex(data, copy=False)
        else:
            index = TimedeltaIndex(data.view(kind), copy=False)
    elif kind == "date":
        try:
            index = np.asarray([date.fromordinal(v) for v in data], dtype=object)
        except ValueError:
            index = np.asarray([date.fromtimestamp(v) for v in data], dtype=object)
    elif kind in ("integer", "float", "bool"):
        index = np.asarray(data)
    elif kind in ("string"):
        index = _unconvert_string_array(
            data, nan_rep=None, encoding=encoding, errors=errors
        )
    elif kind == "object":
        index = np.asarray(data[0])
    else:  # pragma: no cover
        raise ValueError(f"unrecognized index type {kind}")
    return index

