
def test_info_int_columns(using_infer_string):
    # GH#37245
    df = DataFrame({1: [1, 2], 2: [2, 3]}, index=["A", "B"])
    buf = StringIO()
    df.info(show_counts=True, buf=buf)
    result = buf.getvalue()
    expected = textwrap.dedent(
        f"""\
        <class 'pandas.DataFrame'>
        Index: 2 entries, A to B
        Data columns (total 2 columns):
         #   Column  Non-Null Count  Dtype
        ---  ------  --------------  -----
         0   1       2 non-null      int64
         1   2       2 non-null      int64
        dtypes: int64(2)
        memory usage: {"50.0" if using_infer_string and HAS_PYARROW else "48.0+"} bytes
        """
    )
    assert result == expected

