
def _maybe_normalize_endpoints(
    start: _TimestampNoneT1, end: _TimestampNoneT2, normalize: bool
) -> tuple[_TimestampNoneT1, _TimestampNoneT2]:
    if normalize:
        if start is not None:
            start = start.normalize()

        if end is not None:
            end = end.normalize()

    return start, end

