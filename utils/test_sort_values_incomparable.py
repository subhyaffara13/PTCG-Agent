
def test_sort_values_incomparable():
    # GH48495
    mi = MultiIndex.from_arrays(
        [
            [1, Timestamp("2000-01-01")],
            [3, 4],
        ]
    )
    match = "'<' not supported between instances of 'Timestamp' and 'int'"
    with pytest.raises(TypeError, match=match):
        mi.sort_values()

