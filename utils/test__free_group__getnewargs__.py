
def test_FreeGroup__getnewargs__():
    x, y, z = map(Symbol, "xyz")
    assert FreeGroup("x, y, z").__getnewargs__() == ((x, y, z),)

