
def test_agg_lambda_pyarrow_struct_to_object_dtype_conversion():
    # GH#59601
    import pyarrow as pa

    df = DataFrame(
        {
            "A": ["c1", "c2", "c3"],
            "B": pd.array([100, 200, 255], dtype="int64[pyarrow]"),
        }
    )
    gb = df.groupby("A")
    result = gb.agg(lambda x: {"number": 1})

    arr = pa.array([{"number": 1}, {"number": 1}, {"number": 1}])
    expected = DataFrame(
        {"B": ArrowExtensionArray(arr)},
        index=Index(["c1", "c2", "c3"], name="A"),
    )

    tm.assert_frame_equal(result, expected)

