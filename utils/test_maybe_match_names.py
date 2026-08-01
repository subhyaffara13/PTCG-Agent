
def test_maybe_match_names(data, names, expected):
    # GH#38323
    mi = MultiIndex.from_tuples([], names=["a", "b"])
    mi2 = MultiIndex.from_tuples([data], names=names)
    result = mi._maybe_match_names(mi2)
    assert result == expected

