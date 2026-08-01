
def test_truncate_multiindex():
    # GH 34564 for MultiIndex level names check
    major_axis = Index(list(range(4)))
    minor_axis = Index(list(range(2)))

    major_codes = np.array([0, 0, 1, 2, 3, 3])
    minor_codes = np.array([0, 1, 0, 1, 0, 1])

    index = MultiIndex(
        levels=[major_axis, minor_axis],
        codes=[major_codes, minor_codes],
        names=["L1", "L2"],
    )

    result = index.truncate(before=1)
    assert "foo" not in result.levels[0]
    assert 1 in result.levels[0]
    assert index.names == result.names

    result = index.truncate(after=1)
    assert 2 not in result.levels[0]
    assert 1 in result.levels[0]
    assert index.names == result.names

    result = index.truncate(before=1, after=2)
    assert len(result.levels[0]) == 2
    assert index.names == result.names

    msg = "after < before"
    with pytest.raises(ValueError, match=msg):
        index.truncate(3, 1)

