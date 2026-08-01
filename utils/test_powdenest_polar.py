
def test_powdenest_polar():
    x, y, z = symbols('x y z', polar=True)
    a, b, c = symbols('a b c')
    assert powdenest((x*y*z)**a) == x**a*y**a*z**a
    assert powdenest((x**a*y**b)**c) == x**(a*c)*y**(b*c)
    assert powdenest(((x**a)**b*y**c)**c) == x**(a*b*c)*y**(c**2)

