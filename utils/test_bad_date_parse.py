
def test_bad_date_parse(all_parsers, cache, value):
    # if we have an invalid date make sure that we handle this with
    # and w/o the cache properly
    parser = all_parsers
    s = StringIO((f"{value},\n") * (start_caching_at + 1))

    parser.read_csv(
        s,
        header=None,
        names=["foo", "bar"],
        parse_dates=["foo"],
        cache_dates=cache,
    )

