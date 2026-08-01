
def test_join_level_corner_case(idx):
    # some corner cases
    index = Index(["three", "one", "two"])
    result = index.join(idx, level="second")
    assert isinstance(result, MultiIndex)

    with pytest.raises(TypeError, match="Join.*MultiIndex.*ambiguous"):
        idx.join(idx, level=1)

