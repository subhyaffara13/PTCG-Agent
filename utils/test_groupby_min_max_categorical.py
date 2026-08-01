
def test_groupby_min_max_categorical(func):
    # GH: 52151
    df = DataFrame(
        {
            "col1": pd.Categorical(["A"], categories=list("AB"), ordered=True),
            "col2": pd.Categorical([1], categories=[1, 2], ordered=True),
            "value": 0.1,
        }
    )
    result = getattr(df.groupby("col1", observed=False), func)()

    idx = pd.CategoricalIndex(data=["A", "B"], name="col1", ordered=True)
    expected = DataFrame(
        {
            "col2": pd.Categorical([1, None], categories=[1, 2], ordered=True),
            "value": [0.1, None],
        },
        index=idx,
    )
    tm.assert_frame_equal(result, expected)

