
def resolve_constr(cls):  # type: ignore[no-untyped-def]  # pragma: no cover
    min_size = cls.min_length or 0
    max_size = cls.max_length

    if cls.regex is None and not cls.strip_whitespace:
        return st.text(min_size=min_size, max_size=max_size)

    if cls.regex is not None:
        strategy = st.from_regex(cls.regex)
        if cls.strip_whitespace:
            strategy = strategy.filter(lambda s: s == s.strip())
    elif cls.strip_whitespace:
        repeats = '{{{},{}}}'.format(
            min_size - 2 if min_size > 2 else 0,
            max_size - 2 if (max_size or 0) > 2 else '',
        )
        if min_size >= 2:
            strategy = st.from_regex(rf'\W.{repeats}\W')
        elif min_size == 1:
            strategy = st.from_regex(rf'\W(.{repeats}\W)?')
        else:
            assert min_size == 0
            strategy = st.from_regex(rf'(\W(.{repeats}\W)?)?')

    if min_size == 0 and max_size is None:
        return strategy
    elif max_size is None:
        return strategy.filter(lambda s: min_size <= len(s))
    return strategy.filter(lambda s: min_size <= len(s) <= max_size)

