
def test_agg_lambda_pyarrow_dtype_conversion(dtype):
    # GH#59601
    # Test PyArrow dtype conversion back to PyArrow dtype
    df = DataFrame(
        {
            "A": ["c1", "c2", "c3", "c1", "c2", "c3"],
            "B": pd.array([100, 200, 255, 0, 199, 40392], dtype=dtype),
        }
    )
    gb = df.groupby("A")
    result = gb.agg(lambda x: x.min())

    expected = DataFrame(
        {"B": pd.array([0, 199, 255], dtype=dtype)},
        index=Index(["c1", "c2", "c3"], name="A"),
    )
    tm.assert_frame_equal(result, expected)

