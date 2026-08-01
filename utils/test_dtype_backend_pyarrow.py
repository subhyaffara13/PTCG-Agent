
def test_dtype_backend_pyarrow(all_parsers, request):
    # GH#36712
    pa = pytest.importorskip("pyarrow")
    parser = all_parsers

    data = """a,b,c,d,e,f,g,h,i,j
1,2.5,True,a,,,,,12-31-2019,
3,4.5,False,b,6,7.5,True,a,12-31-2019,
"""
    result = parser.read_csv(StringIO(data), dtype_backend="pyarrow", parse_dates=["i"])
    expected = DataFrame(
        {
            "a": pd.Series([1, 3], dtype="int64[pyarrow]"),
            "b": pd.Series([2.5, 4.5], dtype="float64[pyarrow]"),
            "c": pd.Series([True, False], dtype="bool[pyarrow]"),
            "d": pd.Series(["a", "b"], dtype=pd.ArrowDtype(pa.string())),
            "e": pd.Series([pd.NA, 6], dtype="int64[pyarrow]"),
            "f": pd.Series([pd.NA, 7.5], dtype="float64[pyarrow]"),
            "g": pd.Series([pd.NA, True], dtype="bool[pyarrow]"),
            "h": pd.Series(
                [pd.NA, "a"],
                dtype=pd.ArrowDtype(pa.string()),
            ),
            "i": pd.Series([Timestamp("2019-12-31")] * 2),
            "j": pd.Series([pd.NA, pd.NA], dtype="null[pyarrow]"),
        }
    )
    tm.assert_frame_equal(result, expected)

