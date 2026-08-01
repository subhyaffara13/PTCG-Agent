
def test_FreeGroup__init__():
    x, y, z = map(Symbol, "xyz")

    assert len(FreeGroup("x, y, z").generators) == 3
    assert len(FreeGroup(x).generators) == 1
    assert len(FreeGroup(("x", "y", "z"))) == 3
    assert len(FreeGroup((x, y, z)).generators) == 3

