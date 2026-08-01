
def test_transform_groupby_kernel_frame(request, float_frame, op):
    if op == "ngroup":
        request.applymarker(
            pytest.mark.xfail(raises=ValueError, reason="ngroup not valid for NDFrame")
        )

    # GH 35964

    args = [0.0] if op == "fillna" else []
    ones = np.ones(float_frame.shape[0])
    gb = float_frame.groupby(ones)

    warn = FutureWarning if op == "fillna" else None
    op_msg = "DataFrameGroupBy.fillna is deprecated"
    with tm.assert_produces_warning(warn, match=op_msg):
        expected = gb.transform(op, *args)

    result = float_frame.transform(op, 0, *args)
    tm.assert_frame_equal(result, expected)

    # same thing, but ensuring we have multiple blocks
    assert "E" not in float_frame.columns
    float_frame["E"] = float_frame["A"].copy()
    assert len(float_frame._mgr.blocks) > 1

    ones = np.ones(float_frame.shape[0])
    gb2 = float_frame.groupby(ones)
    expected2 = gb2.transform(op, *args)
    result2 = float_frame.transform(op, 0, *args)
    tm.assert_frame_equal(result2, expected2)

