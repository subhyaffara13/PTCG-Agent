
def test_numba_vs_python_string_index():
    # GH#56189
    df = DataFrame(
        1,
        index=Index(["a", "b"], dtype=pd.StringDtype(na_value=np.nan)),
        columns=Index(["x", "y"], dtype=pd.StringDtype(na_value=np.nan)),
    )
    func = lambda x: x
    result = df.apply(func, engine="numba", axis=0)
    expected = df.apply(func, engine="python", axis=0)
    tm.assert_frame_equal(
        result, expected, check_column_type=False, check_index_type=False
    )

