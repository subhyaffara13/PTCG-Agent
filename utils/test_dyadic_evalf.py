
def test_dyadic_evalf():
    N = ReferenceFrame('N')
    a = pi * (N.x | N.x)
    assert a.evalf(3) == Float('3.1416', 3) * (N.x | N.x)
    s = symbols('s')
    a = 5 * s * pi* (N.x | N.x)
    assert a.evalf(2) == Float('5', 2) * Float('3.1416', 2) * s * (N.x | N.x)
    assert a.evalf(9, subs={s: 5.124}) == Float('80.48760378', 9) * (N.x | N.x)

