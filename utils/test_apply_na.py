
def test_apply_na(dropna):
    # GH#28984
    df = DataFrame(
        {"grp": [1, 1, 2, 2], "y": [1, 0, 2, 5], "z": [1, 2, np.nan, np.nan]}
    )
    dfgrp = df.groupby("grp", dropna=dropna)
    result = dfgrp.apply(lambda grp_df: grp_df.nlargest(1, "z"))
    expected = dfgrp.apply(lambda x: x.sort_values("z", ascending=False).head(1))
    tm.assert_frame_equal(result, expected)

