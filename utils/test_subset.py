
def test_subset():
    a = Subset(['c', 'd'], ['a', 'b', 'c', 'd'])
    assert a.next_binary() == Subset(['b'], ['a', 'b', 'c', 'd'])
    assert a.prev_binary() == Subset(['c'], ['a', 'b', 'c', 'd'])
    assert a.next_lexicographic() == Subset(['d'], ['a', 'b', 'c', 'd'])
    assert a.prev_lexicographic() == Subset(['c'], ['a', 'b', 'c', 'd'])
    assert a.next_gray() == Subset(['c'], ['a', 'b', 'c', 'd'])
    assert a.prev_gray() == Subset(['d'], ['a', 'b', 'c', 'd'])
    assert a.rank_binary == 3
    assert a.rank_lexicographic == 14
    assert a.rank_gray == 2
    assert a.cardinality == 16
    assert a.size == 2
    assert Subset.bitlist_from_subset(a, ['a', 'b', 'c', 'd']) == '0011'

    a = Subset([2, 5, 7], [1, 2, 3, 4, 5, 6, 7])
    assert a.next_binary() == Subset([2, 5, 6], [1, 2, 3, 4, 5, 6, 7])
    assert a.prev_binary() == Subset([2, 5], [1, 2, 3, 4, 5, 6, 7])
    assert a.next_lexicographic() == Subset([2, 6], [1, 2, 3, 4, 5, 6, 7])
    assert a.prev_lexicographic() == Subset([2, 5, 6, 7], [1, 2, 3, 4, 5, 6, 7])
    assert a.next_gray() == Subset([2, 5, 6, 7], [1, 2, 3, 4, 5, 6, 7])
    assert a.prev_gray() == Subset([2, 5], [1, 2, 3, 4, 5, 6, 7])
    assert a.rank_binary == 37
    assert a.rank_lexicographic == 93
    assert a.rank_gray == 57
    assert a.cardinality == 128

    superset = ['a', 'b', 'c', 'd']
    assert Subset.unrank_binary(4, superset).rank_binary == 4
    assert Subset.unrank_gray(10, superset).rank_gray == 10

    superset = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert Subset.unrank_binary(33, superset).rank_binary == 33
    assert Subset.unrank_gray(25, superset).rank_gray == 25

    a = Subset([], ['a', 'b', 'c', 'd'])
    i = 1
    while a.subset != Subset(['d'], ['a', 'b', 'c', 'd']).subset:
        a = a.next_lexicographic()
        i = i + 1
    assert i == 16

    i = 1
    while a.subset != Subset([], ['a', 'b', 'c', 'd']).subset:
        a = a.prev_lexicographic()
        i = i + 1
    assert i == 16

    raises(ValueError, lambda: Subset(['a', 'b'], ['a']))
    raises(ValueError, lambda: Subset(['a'], ['b', 'c']))
    raises(ValueError, lambda: Subset.subset_from_bitlist(['a', 'b'], '010'))

    assert Subset(['a'], ['a', 'b']) != Subset(['b'], ['a', 'b'])
    assert Subset(['a'], ['a', 'b']) != Subset(['a'], ['a', 'c'])


def test_subset():
    # GH 46383
    df = DataFrame({"c1": ["a", "b", "c"], "c2": ["x", "y", "y"]}, index=[0, 1, 1])
    result = df.groupby(level=0).value_counts(subset=["c2"])
    expected = Series(
        [1, 2],
        index=MultiIndex.from_arrays([[0, 1], ["x", "y"]], names=[None, "c2"]),
        name="count",
    )
    tm.assert_series_equal(result, expected)

