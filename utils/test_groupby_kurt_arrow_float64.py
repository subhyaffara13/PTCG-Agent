
def test_groupby_kurt_arrow_float64(dtype):
    # GH#40139
    # Test groupby.kurt() with float64[pyarrow] and Float64 dtypes
    df = pd.DataFrame(
        {
            "x": [1.0, pd.NA, 3.2, 4.8, 2.3, 1.9, 8.9],
            "y": [1.6, 3.3, 3.2, 6.8, 1.3, 2.9, 9.0],
        },
        dtype=dtype,
    )
    gb = df.groupby(by=lambda x: 0)

    result = gb.kurt()
    expected = pd.DataFrame({"x": [2.1644713], "y": [0.1513969]}, dtype=dtype)
    tm.assert_almost_equal(result, expected)

