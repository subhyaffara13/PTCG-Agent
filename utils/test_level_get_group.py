
def test_level_get_group(observed):
    # GH15155
    df = DataFrame(
        data=np.arange(2, 22, 2),
        index=MultiIndex(
            levels=[CategoricalIndex(["a", "b"]), range(10)],
            codes=[[0] * 5 + [1] * 5, range(10)],
            names=["Index1", "Index2"],
        ),
    )
    g = df.groupby(level=["Index1"], observed=observed)

    # expected should equal test.loc[["a"]]
    # GH15166
    expected = DataFrame(
        data=np.arange(2, 12, 2),
        index=MultiIndex(
            levels=[CategoricalIndex(["a", "b"]), range(5)],
            codes=[[0] * 5, range(5)],
            names=["Index1", "Index2"],
        ),
    )
    result = g.get_group(("a",))
    tm.assert_frame_equal(result, expected)

