
def test_quantile_array2():
    # https://github.com/pandas-dev/pandas/pull/28085#issuecomment-524066959
    arr = np.random.default_rng(2).integers(0, 5, size=(10, 3), dtype=np.int64)
    df = DataFrame(arr, columns=list("ABC"))
    result = df.groupby("A").quantile([0.3, 0.7])
    expected = DataFrame(
        {
            "B": [2.0, 2.0, 2.3, 2.7, 0.3, 0.7, 3.2, 4.0, 0.3, 0.7],
            "C": [1.0, 1.0, 1.9, 3.0999999999999996, 0.3, 0.7, 2.6, 3.0, 1.2, 2.8],
        },
        index=pd.MultiIndex.from_product(
            [[0, 1, 2, 3, 4], [0.3, 0.7]], names=["A", None]
        ),
    )
    tm.assert_frame_equal(result, expected)

