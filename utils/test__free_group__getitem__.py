
def test_FreeGroup__getitem__():
    assert F[0:] == FreeGroup("x, y, z")
    assert F[1:] == FreeGroup("y, z")
    assert F[2:] == FreeGroup("z")

