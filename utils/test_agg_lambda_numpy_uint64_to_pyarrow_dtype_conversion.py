
def test_agg_lambda_numpy_uint64_to_pyarrow_dtype_conversion():
    # GH#59601
    df = DataFrame(
        {
            "A": ["c1", "c2", "c3"],
            "B": pd.array([100, 200, 255], dtype="uint64[pyarrow]"),
        }
    )
    gb = df.groupby("A")
    result = gb.agg(lambda x: np.uint64(x.sum()))

    expected = DataFrame(
        {
            "B": pd.array([100, 200, 255], dtype="uint64[pyarrow]"),
        },
        index=Index(["c1", "c2", "c3"], name="A"),
    )
    tm.assert_frame_equal(result, expected)

