
def test_dyadic_subs():
    N = ReferenceFrame('N')
    s = symbols('s')
    a = s*(N.x | N.x)
    assert a.subs({s: 2}) == 2*(N.x | N.x)

