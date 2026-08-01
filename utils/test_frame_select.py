
def test_frame_select(temp_hdfstore, request):
    df = DataFrame(
        np.random.default_rng(2).standard_normal((10, 4)),
        columns=Index(list("ABCD")),
        index=date_range("2000-01-01", periods=10, freq="B", unit="ns"),
    )

    temp_hdfstore.put("frame", df, format="table")
    date = df.index[len(df) // 2]

    crit1 = Term("index>=date")
    assert crit1.env.scope["date"] == date

    crit2 = "columns=['A', 'D']"
    crit3 = "columns=A"

    request.applymarker(
        pytest.mark.xfail(
            PY312,
            reason="AST change in PY312",
            raises=TypeError,
        )
    )
    result = temp_hdfstore.select("frame", [crit1, crit2])
    expected = df.loc[date:, ["A", "D"]]
    tm.assert_frame_equal(result, expected)

    result = temp_hdfstore.select("frame", [crit3])
    expected = df.loc[:, ["A"]]
    tm.assert_frame_equal(result, expected)

    # invalid terms
    df = DataFrame(
        np.random.default_rng(2).standard_normal((10, 4)),
        columns=Index(list("ABCD")),
        index=date_range("2000-01-01", periods=10, freq="B", unit="ns"),
    )
    temp_hdfstore.append("df_time", df)
    msg = "day is out of range for month: 0"
    with pytest.raises(ValueError, match=msg):
        temp_hdfstore.select("df_time", "index>0")

