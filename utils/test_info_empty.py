
def test_info_empty():
    # GH #45494
    df = DataFrame()
    buf = StringIO()
    df.info(buf=buf)
    result = buf.getvalue()
    expected = textwrap.dedent(
        """\
        <class 'pandas.DataFrame'>
        RangeIndex: 0 entries
        Empty DataFrame\n"""
    )
    assert result == expected

