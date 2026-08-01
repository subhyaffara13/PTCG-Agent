
def test_37692(indexer_al):
    # GH#37692
    ser = Series([1, 2, 3], index=["a", "b", "c"])
    with pytest.raises(TypeError, match="Invalid value"):
        indexer_al(ser)["b"] = "test"

