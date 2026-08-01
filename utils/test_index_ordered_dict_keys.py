
def test_index_ordered_dict_keys():
    # GH 22077

    param_index = OrderedDict(
        [
            ((("a", "b"), ("c", "d")), 1),
            ((("a", None), ("c", "d")), 2),
        ]
    )
    series = Series([1, 2], index=param_index.keys())
    expected = Series(
        [1, 2],
        index=MultiIndex.from_tuples(
            [(("a", "b"), ("c", "d")), (("a", None), ("c", "d"))]
        ),
    )
    tm.assert_series_equal(series, expected)

