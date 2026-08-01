
def test_grouping_with_categorical_interval_columns():
    # GH#34164
    df = DataFrame({"x": [0.1, 0.2, 0.3, -0.4, 0.5], "w": ["a", "b", "a", "c", "a"]})
    qq = pd.qcut(df["x"], q=np.linspace(0, 1, 5))
    result = df.groupby([qq, "w"], observed=False)["x"].agg("mean")
    categorical_index_level_1 = Categorical(
        [
            Interval(-0.401, 0.1, closed="right"),
            Interval(0.1, 0.2, closed="right"),
            Interval(0.2, 0.3, closed="right"),
            Interval(0.3, 0.5, closed="right"),
        ],
        ordered=True,
    )
    index_level_2 = ["a", "b", "c"]
    mi = MultiIndex.from_product(
        [categorical_index_level_1, index_level_2], names=["x", "w"]
    )
    expected = Series(
        np.array(
            [
                0.1,
                np.nan,
                -0.4,
                np.nan,
                0.2,
                np.nan,
                0.3,
                np.nan,
                np.nan,
                0.5,
                np.nan,
                np.nan,
            ]
        ),
        index=mi,
        name="x",
    )
    tm.assert_series_equal(result, expected)

