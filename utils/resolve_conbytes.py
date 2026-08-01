
def resolve_conbytes(cls):  # type: ignore[no-untyped-def]  # pragma: no cover
    min_size = cls.min_length or 0
    max_size = cls.max_length
    if not cls.strip_whitespace:
        return st.binary(min_size=min_size, max_size=max_size)
    # Fun with regex to ensure we neither start nor end with whitespace
    repeats = '{{{},{}}}'.format(
        min_size - 2 if min_size > 2 else 0,
        max_size - 2 if (max_size or 0) > 2 else '',
    )
    if min_size >= 2:
        pattern = rf'\W.{repeats}\W'
    elif min_size == 1:
        pattern = rf'\W(.{repeats}\W)?'
    else:
        assert min_size == 0
        pattern = rf'(\W(.{repeats}\W)?)?'
    return st.from_regex(pattern.encode(), fullmatch=True)

