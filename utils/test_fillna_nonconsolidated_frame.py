
def test_fillna_nonconsolidated_frame():
    # https://github.com/pandas-dev/pandas/issues/36495
    df = DataFrame(
        [
            [1, 1, 1, 1.0],
            [2, 2, 2, 2.0],
            [3, 3, 3, 3.0],
        ],
        columns=["i1", "i2", "i3", "f1"],
    )
    df_nonconsol = df.pivot(index="i1", columns="i2")
    result = df_nonconsol.fillna(0)
    assert result.isna().sum().sum() == 0

