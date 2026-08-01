
def test_info_series(
    lexsorted_two_level_string_multiindex, verbose, using_infer_string
):
    index = lexsorted_two_level_string_multiindex
    ser = Series(range(len(index)), index=index, name="sth")
    buf = StringIO()
    ser.info(verbose=verbose, buf=buf)
    result = buf.getvalue()

    expected = textwrap.dedent(
        """\
        <class 'pandas.Series'>
        MultiIndex: 10 entries, ('foo', 'one') to ('qux', 'three')
        """
    )
    if verbose:
        expected += textwrap.dedent(
            """\
            Series name: sth
            Non-Null Count  Dtype
            --------------  -----
            10 non-null     int64
            """
        )
    qualifier = "" if using_infer_string and HAS_PYARROW else "+"
    expected += textwrap.dedent(
        f"""\
        dtypes: int64(1)
        memory usage: {ser.memory_usage()}.0{qualifier} bytes
        """
    )
    assert result == expected

