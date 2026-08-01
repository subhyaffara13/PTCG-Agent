
def test_select_filter_corner(temp_hdfstore, request):
    df = DataFrame(np.random.default_rng(2).standard_normal((50, 100)))
    df.index = [f"{c:3d}" for c in df.index]
    df.columns = [f"{c:3d}" for c in df.columns]

    temp_hdfstore.put("frame", df, format="table")

    request.applymarker(
        pytest.mark.xfail(
            PY312,
            reason="AST change in PY312",
            raises=ValueError,
        )
    )
    crit = "columns=df.columns[:75]"
    result = temp_hdfstore.select("frame", [crit])
    tm.assert_frame_equal(result, df.loc[:, df.columns[:75]])

    crit = "columns=df.columns[:75:2]"
    result = temp_hdfstore.select("frame", [crit])
    tm.assert_frame_equal(result, df.loc[:, df.columns[:75:2]])

