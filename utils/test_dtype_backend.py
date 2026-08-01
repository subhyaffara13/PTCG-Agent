
def test_dtype_backend(string_storage, dtype_backend):
    # GH#50289
    data = """a  b    c      d  e     f  g    h  i
1  2.5  True  a
3  4.5  False b  True  6  7.5  a"""
    with pd.option_context("mode.string_storage", string_storage):
        result = read_fwf(StringIO(data), dtype_backend=dtype_backend)

    if dtype_backend == "pyarrow":
        pa = pytest.importorskip("pyarrow")
        string_dtype = pd.ArrowDtype(pa.string())
    else:
        string_dtype = pd.StringDtype(string_storage)

    expected = DataFrame(
        {
            "a": pd.Series([1, 3], dtype="Int64"),
            "b": pd.Series([2.5, 4.5], dtype="Float64"),
            "c": pd.Series([True, False], dtype="boolean"),
            "d": pd.Series(["a", "b"], dtype=string_dtype),
            "e": pd.Series([pd.NA, True], dtype="boolean"),
            "f": pd.Series([pd.NA, 6], dtype="Int64"),
            "g": pd.Series([pd.NA, 7.5], dtype="Float64"),
            "h": pd.Series([None, "a"], dtype=string_dtype),
            "i": pd.Series([pd.NA, pd.NA], dtype="Int64"),
        }
    )
    if dtype_backend == "pyarrow":
        pa = pytest.importorskip("pyarrow")
        from pandas.arrays import ArrowExtensionArray

        expected = DataFrame(
            {
                col: ArrowExtensionArray(pa.array(expected[col], from_pandas=True))
                for col in expected.columns
            }
        )
        expected["i"] = ArrowExtensionArray(pa.array([None, None]))

    # the storage of the str columns' Index is also affected by the
    # string_storage setting -> ignore that for checking the result
    tm.assert_frame_equal(result, expected, check_column_type=False)


def test_dtype_backend(all_parsers):
    # GH#36712

    parser = all_parsers

    data = """a,b,c,d,e,f,g,h,i,j
1,2.5,True,a,,,,,12-31-2019,
3,4.5,False,b,6,7.5,True,a,12-31-2019,
"""
    result = parser.read_csv(
        StringIO(data), dtype_backend="numpy_nullable", parse_dates=["i"]
    )
    expected = DataFrame(
        {
            "a": pd.Series([1, 3], dtype="Int64"),
            "b": pd.Series([2.5, 4.5], dtype="Float64"),
            "c": pd.Series([True, False], dtype="boolean"),
            "d": pd.Series(["a", "b"], dtype="string"),
            "e": pd.Series([pd.NA, 6], dtype="Int64"),
            "f": pd.Series([pd.NA, 7.5], dtype="Float64"),
            "g": pd.Series([pd.NA, True], dtype="boolean"),
            "h": pd.Series([pd.NA, "a"], dtype="string"),
            "i": pd.Series([Timestamp("2019-12-31")] * 2),
            "j": pd.Series([pd.NA, pd.NA], dtype="Int64"),
        }
    )
    tm.assert_frame_equal(result, expected)

