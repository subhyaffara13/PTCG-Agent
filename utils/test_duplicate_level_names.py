
def test_duplicate_level_names(names):
    # GH18872, GH19029
    mi = MultiIndex.from_product([[0, 1]] * 3, names=names)
    assert mi.names == names

    # With .rename()
    mi = MultiIndex.from_product([[0, 1]] * 3)
    mi = mi.rename(names)
    assert mi.names == names

    # With .rename(., level=)
    mi.rename(names[1], level=1, inplace=True)
    mi = mi.rename([names[0], names[2]], level=[0, 2])
    assert mi.names == names

