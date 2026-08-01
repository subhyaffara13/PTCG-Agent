
def test_preserve_categorical_dtype(col):
    # GH13743, GH13854
    df = DataFrame(
        {
            "A": [1, 2, 1, 1, 2],
            "B": [10, 16, 22, 28, 34],
            "C1": Categorical(list("abaab"), categories=list("bac"), ordered=False),
            "C2": Categorical(list("abaab"), categories=list("bac"), ordered=True),
        }
    )
    # single grouper
    exp_full = DataFrame(
        {
            "A": [2.0, 1.0, np.nan],
            "B": [25.0, 20.0, np.nan],
            "C1": Categorical(list("bac"), categories=list("bac"), ordered=False),
            "C2": Categorical(list("bac"), categories=list("bac"), ordered=True),
        }
    )
    result1 = df.groupby(by=col, as_index=False, observed=False).mean(numeric_only=True)
    result2 = (
        df.groupby(by=col, as_index=True, observed=False)
        .mean(numeric_only=True)
        .reset_index()
    )
    expected = exp_full.reindex(columns=result1.columns)
    tm.assert_frame_equal(result1, expected)
    tm.assert_frame_equal(result2, expected)

