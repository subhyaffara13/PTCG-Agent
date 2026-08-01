
def test_bad_date_parse_with_warning(all_parsers, cache):
    # if we have an invalid date make sure that we handle this with
    # and w/o the cache properly.
    parser = all_parsers
    s = StringIO(("0,\n") * (start_caching_at + 1))

    if parser.engine == "pyarrow":
        # pyarrow reads "0" as 0 (of type int64), and so
        # pandas doesn't try to guess the datetime format
        # TODO: parse dates directly in pyarrow, see
        # https://github.com/pandas-dev/pandas/issues/48017
        warn = None
    elif cache:
        # Note: warning is not raised if 'cache_dates', because here there is only a
        # single unique date and hence no risk of inconsistent parsing.
        warn = None
    else:
        warn = UserWarning
    parser.read_csv_check_warnings(
        warn,
        "Could not infer format",
        s,
        header=None,
        names=["foo", "bar"],
        parse_dates=["foo"],
        cache_dates=cache,
        raise_on_extra_warnings=False,
    )

