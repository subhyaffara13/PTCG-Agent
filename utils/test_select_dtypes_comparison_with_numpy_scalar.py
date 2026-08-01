
def test_select_dtypes_comparison_with_numpy_scalar(temp_hdfstore, request):
    # GH 11283
    df = DataFrame(
        1.1 * np.arange(120).reshape((30, 4)),
        columns=Index(list("ABCD")),
        index=Index([f"i-{i}" for i in range(30)]),
    )

    expected = df[df["A"] > 0]

    temp_hdfstore.append("df", df, data_columns=True)
    request.applymarker(
        pytest.mark.xfail(
            PY312,
            reason="AST change in PY312",
            raises=ValueError,
        )
    )
    np_zero = np.float64(0)  # noqa: F841
    result = temp_hdfstore.select("df", where=["A>np_zero"])
    tm.assert_frame_equal(expected, result)

