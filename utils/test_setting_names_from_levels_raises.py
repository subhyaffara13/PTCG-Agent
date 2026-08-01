
def test_setting_names_from_levels_raises():
    idx = MultiIndex.from_product([["a"], [1, 2]], names=["a", "b"])
    with pytest.raises(RuntimeError, match="set_names"):
        idx.levels[0].name = "foo"

    with pytest.raises(RuntimeError, match="set_names"):
        idx.levels[1].name = "foo"

    new = pd.Series(1, index=idx.levels[0])
    with pytest.raises(RuntimeError, match="set_names"):
        new.index.name = "bar"

    assert pd.Index._no_setting_name is False
    assert pd.RangeIndex._no_setting_name is False

