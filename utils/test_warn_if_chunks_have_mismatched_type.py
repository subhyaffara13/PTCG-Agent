
def test_warn_if_chunks_have_mismatched_type(
    all_parsers, using_infer_string, monkeypatch
):
    warning_type = None
    parser = all_parsers
    heuristic = 2**3
    size = 10

    # see gh-3866: if chunks are different types and can't
    # be coerced using numerical types, then issue warning.
    if parser.engine == "c" and parser.low_memory:
        warning_type = DtypeWarning
        # Use a size to hit warning path dictated by DEFAULT_BUFFER_HEURISTIC
        # monkeypatched below
        size = heuristic - 1

    integers = [str(i) for i in range(size)]
    data = "a\n" + "\n".join([*integers, "a", "b", *integers])

    buf = StringIO(data)

    if parser.engine == "pyarrow":
        df = parser.read_csv(
            buf,
        )
    else:
        with monkeypatch.context() as m:
            m.setattr(libparsers, "DEFAULT_BUFFER_HEURISTIC", heuristic)
            df = parser.read_csv_check_warnings(
                warning_type,
                r"Columns \(0: a\) have mixed types. "
                "Specify dtype option on import or set low_memory=False.",
                buf,
            )
    if parser.engine == "c" and parser.low_memory:
        assert df.a.dtype == object
    elif using_infer_string:
        assert df.a.dtype == "str"
    else:
        assert df.a.dtype == object

