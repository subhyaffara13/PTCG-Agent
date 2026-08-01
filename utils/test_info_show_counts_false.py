
def test_info_show_counts_false():
    s = Series([1])
    buf = StringIO()
    s.info(buf=buf, show_counts=False)
    result = buf.getvalue()
    memory_bytes = float(s.memory_usage())
    expected = textwrap.dedent(
        f"""\
    <class 'pandas.Series'>
    RangeIndex: 1 entries, 0 to 0
    Series name: None
    Dtype
    -----
    int64
    dtypes: int64(1)
    memory usage: {memory_bytes} bytes"""
    )
    assert result.strip() == expected.strip()

