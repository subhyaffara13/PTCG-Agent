
def test_info_memory():
    s = Series([1, 2], dtype="i8")
    buf = StringIO()
    s.info(buf=buf)
    result = buf.getvalue()
    memory_bytes = float(s.memory_usage())
    expected = textwrap.dedent(
        f"""\
    <class 'pandas.Series'>
    RangeIndex: 2 entries, 0 to 1
    Series name: None
    Non-Null Count  Dtype
    --------------  -----
    2 non-null      int64
    dtypes: int64(1)
    memory usage: {memory_bytes} bytes
    """
    )
    assert result == expected


def test_info_memory():
    # https://github.com/pandas-dev/pandas/issues/21056
    df = DataFrame({"a": Series([1, 2], dtype="i8")})
    buf = StringIO()
    df.info(buf=buf)
    result = buf.getvalue()
    bytes = float(df.memory_usage().sum())
    expected = textwrap.dedent(
        f"""\
    <class 'pandas.DataFrame'>
    RangeIndex: 2 entries, 0 to 1
    Data columns (total 1 columns):
     #   Column  Non-Null Count  Dtype
    ---  ------  --------------  -----
     0   a       2 non-null      int64
    dtypes: int64(1)
    memory usage: {bytes} bytes
    """
    )
    assert result == expected

