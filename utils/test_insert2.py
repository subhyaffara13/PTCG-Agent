
def test_insert2():
    # GH9250
    idx = (
        [("test1", i) for i in range(5)]
        + [("test2", i) for i in range(6)]
        + [("test", 17), ("test", 18)]
    )

    left = pd.Series(np.linspace(0, 10, 11), MultiIndex.from_tuples(idx[:-2]))

    left.loc[("test", 17)] = 11
    left.loc[("test", 18)] = 12

    right = pd.Series(np.linspace(0, 12, 13), MultiIndex.from_tuples(idx))

    tm.assert_series_equal(left, right)

