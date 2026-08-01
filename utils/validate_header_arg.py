
def validate_header_arg(header: object) -> None:
    if header is None:
        return
    if is_integer(header):
        header = cast(int, header)
        if header < 0:
            # GH 27779
            raise ValueError(
                "Passing negative integer to header is invalid. "
                "For no header, use header=None instead"
            )
        return
    if is_list_like(header, allow_sets=False):
        header = cast(Sequence, header)
        if not all(map(is_integer, header)):
            raise ValueError("header must be integer or list of integers")
        if any(i < 0 for i in header):
            raise ValueError("cannot specify multi-index header with negative integers")
        return
    if is_bool(header):
        raise TypeError(
            "Passing a bool to header is invalid. Use header=None for no header or "
            "header=int or list-like of ints to specify "
            "the row(s) making up the column names"
        )
    # GH 16338
    raise ValueError("header must be integer or list of integers")

