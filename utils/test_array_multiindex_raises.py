
def test_array_multiindex_raises():
    idx = pd.MultiIndex.from_product([["A"], ["a", "b"]])
    msg = "MultiIndex has no single backing array"
    with pytest.raises(ValueError, match=msg):
        idx.array

