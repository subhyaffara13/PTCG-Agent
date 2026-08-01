
def test_is_monotonic_increasing():
    i = MultiIndex.from_product([np.arange(10), np.arange(10)], names=["one", "two"])
    assert i.is_monotonic_increasing is True
    assert i._is_strictly_monotonic_increasing is True
    assert Index(i.values).is_monotonic_increasing is True
    assert i._is_strictly_monotonic_increasing is True

    i = MultiIndex.from_product(
        [np.arange(10, 0, -1), np.arange(10)], names=["one", "two"]
    )
    assert i.is_monotonic_increasing is False
    assert i._is_strictly_monotonic_increasing is False
    assert Index(i.values).is_monotonic_increasing is False
    assert Index(i.values)._is_strictly_monotonic_increasing is False

    i = MultiIndex.from_product(
        [np.arange(10), np.arange(10, 0, -1)], names=["one", "two"]
    )
    assert i.is_monotonic_increasing is False
    assert i._is_strictly_monotonic_increasing is False
    assert Index(i.values).is_monotonic_increasing is False
    assert Index(i.values)._is_strictly_monotonic_increasing is False

    i = MultiIndex.from_product([[1.0, np.nan, 2.0], ["a", "b", "c"]])
    assert i.is_monotonic_increasing is False
    assert i._is_strictly_monotonic_increasing is False
    assert Index(i.values).is_monotonic_increasing is False
    assert Index(i.values)._is_strictly_monotonic_increasing is False

    i = MultiIndex(
        levels=[["bar", "baz", "foo", "qux"], ["mom", "next", "zenith"]],
        codes=[[0, 0, 0, 1, 1, 2, 2, 3, 3, 3], [0, 1, 2, 0, 1, 1, 2, 0, 1, 2]],
        names=["first", "second"],
    )
    assert i.is_monotonic_increasing is True
    assert Index(i.values).is_monotonic_increasing is True
    assert i._is_strictly_monotonic_increasing is True
    assert Index(i.values)._is_strictly_monotonic_increasing is True

    # mixed levels, hits the TypeError
    i = MultiIndex(
        levels=[
            [1, 2, 3, 4],
            [
                "gb00b03mlx29",
                "lu0197800237",
                "nl0000289783",
                "nl0000289965",
                "nl0000301109",
            ],
        ],
        codes=[[0, 1, 1, 2, 2, 2, 3], [4, 2, 0, 0, 1, 3, -1]],
        names=["household_id", "asset_id"],
    )

    assert i.is_monotonic_increasing is False
    assert i._is_strictly_monotonic_increasing is False

    # empty
    i = MultiIndex.from_arrays([[], []])
    assert i.is_monotonic_increasing is True
    assert Index(i.values).is_monotonic_increasing is True
    assert i._is_strictly_monotonic_increasing is True
    assert Index(i.values)._is_strictly_monotonic_increasing is True


def test_is_monotonic_increasing():
    # GH#17717
    p0 = Period("2017-09-01")
    p1 = Period("2017-09-02")
    p2 = Period("2017-09-03")

    idx_inc0 = PeriodIndex([p0, p1, p2])
    idx_inc1 = PeriodIndex([p0, p1, p1])
    idx_dec0 = PeriodIndex([p2, p1, p0])
    idx_dec1 = PeriodIndex([p2, p1, p1])
    idx = PeriodIndex([p1, p2, p0])

    assert idx_inc0.is_monotonic_increasing is True
    assert idx_inc1.is_monotonic_increasing is True
    assert idx_dec0.is_monotonic_increasing is False
    assert idx_dec1.is_monotonic_increasing is False
    assert idx.is_monotonic_increasing is False


def test_is_monotonic_increasing(in_vals, out_vals):
    # GH 17015
    source_dict = {
        "A": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"],
        "B": ["a", "a", "a", "b", "b", "b", "c", "c", "c", "d", "d"],
        "C": in_vals,
    }
    df = DataFrame(source_dict)
    result = df.groupby("B").C.is_monotonic_increasing
    index = Index(list("abcd"), name="B")
    expected = Series(index=index, data=out_vals, name="C")
    tm.assert_series_equal(result, expected)

    # Also check result equal to manually taking x.is_monotonic_increasing.
    expected = df.groupby(["B"]).C.apply(lambda x: x.is_monotonic_increasing)
    tm.assert_series_equal(result, expected)

