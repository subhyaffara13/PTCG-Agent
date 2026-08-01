
def test_binary_input_aligns_columns(request, dtype_a, dtype_b):
    if (
        is_extension_array_dtype(dtype_a)
        or isinstance(dtype_a, dict)
        or is_extension_array_dtype(dtype_b)
        or isinstance(dtype_b, dict)
    ):
        request.applymarker(
            pytest.mark.xfail(
                reason="Extension / mixed with multiple inputs not implemented."
            )
        )

    df1 = pd.DataFrame({"A": [1, 2], "B": [3, 4]}).astype(dtype_a)

    if isinstance(dtype_a, dict) and isinstance(dtype_b, dict):
        dtype_b = dtype_b.copy()
        dtype_b["C"] = dtype_b.pop("B")
    df2 = pd.DataFrame({"A": [1, 2], "C": [3, 4]}).astype(dtype_b)
    # As of 2.0, align first before applying the ufunc
    result = np.heaviside(df1, df2)
    expected = np.heaviside(
        np.array([[1, 3, np.nan], [2, 4, np.nan]]),
        np.array([[1, np.nan, 3], [2, np.nan, 4]]),
    )
    expected = pd.DataFrame(expected, index=[0, 1], columns=["A", "B", "C"])
    tm.assert_frame_equal(result, expected)

    result = np.heaviside(df1, df2.values)
    expected = pd.DataFrame([[1.0, 1.0], [1.0, 1.0]], columns=["A", "B"])
    tm.assert_frame_equal(result, expected)

