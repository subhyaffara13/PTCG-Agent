
def test_info_wide():
    s = Series(np.random.default_rng(2).standard_normal(101))
    msg = "Argument `max_cols` can only be passed in DataFrame.info, not Series.info"
    with pytest.raises(ValueError, match=msg):
        s.info(max_cols=1)


def test_info_wide():
    io = StringIO()
    df = DataFrame(np.random.default_rng(2).standard_normal((5, 101)))
    df.info(buf=io)

    io = StringIO()
    df.info(buf=io, max_cols=101)
    result = io.getvalue()
    assert len(result.splitlines()) > 100

    expected = result
    with option_context("display.max_info_columns", 101):
        io = StringIO()
        df.info(buf=io)
        result = io.getvalue()
        assert result == expected

