
def test_FracElement_diff():
    F, x,y,z = field("x,y,z", ZZ)

    assert ((x**2 + y)/(z + 1)).diff(x) == 2*x/(z + 1)

