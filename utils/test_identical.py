
def test_identical(idx):
    mi = idx.copy()
    mi2 = idx.copy()
    assert mi.identical(mi2)

    mi = mi.set_names(["new1", "new2"])
    assert mi.equals(mi2)
    assert not mi.identical(mi2)

    mi2 = mi2.set_names(["new1", "new2"])
    assert mi.identical(mi2)

    mi4 = Index(mi.tolist(), tupleize_cols=False)
    assert not mi.identical(mi4)
    assert mi.equals(mi4)

