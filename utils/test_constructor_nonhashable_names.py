
def test_constructor_nonhashable_names():
    # GH 20527
    levels = [[1, 2], ["one", "two"]]
    codes = [[0, 0, 1, 1], [0, 1, 0, 1]]
    names = (["foo"], ["bar"])
    msg = r"MultiIndex\.name must be a hashable type"
    with pytest.raises(TypeError, match=msg):
        MultiIndex(levels=levels, codes=codes, names=names)

    # With .rename()
    mi = MultiIndex(
        levels=[[1, 2], ["one", "two"]],
        codes=[[0, 0, 1, 1], [0, 1, 0, 1]],
        names=("foo", "bar"),
    )
    renamed = [["fooo"], ["barr"]]
    with pytest.raises(TypeError, match=msg):
        mi.rename(names=renamed)

    # With .set_names()
    with pytest.raises(TypeError, match=msg):
        mi.set_names(names=renamed)

