
def test_is_():
    mi = MultiIndex.from_tuples(zip(range(10), range(10), strict=True))
    assert mi.is_(mi)
    assert mi.is_(mi.view())
    assert mi.is_(mi.view().view().view().view())
    mi2 = mi.view()
    # names are metadata, they don't change id
    mi2.names = ["A", "B"]
    assert mi2.is_(mi)
    assert mi.is_(mi2)

    assert not mi.is_(mi.set_names(["C", "D"]))
    # levels are inherent properties, they change identity
    mi3 = mi2.set_levels([list(range(10)), list(range(10))])
    assert not mi3.is_(mi2)
    # shouldn't change
    assert mi2.is_(mi)
    mi4 = mi3.view()

    # GH 17464 - Remove duplicate MultiIndex levels
    mi4 = mi4.set_levels([list(range(10)), list(range(10))])
    assert not mi4.is_(mi3)
    mi5 = mi.view()
    mi5 = mi5.set_levels(mi5.levels)
    assert not mi5.is_(mi)

