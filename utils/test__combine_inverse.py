
def test__combine_inverse():
    x, y = symbols("x y")
    assert Mul._combine_inverse(x*I*y, x*I) == y
    assert Mul._combine_inverse(x*x**(1 + y), x**(1 + y)) == x
    assert Mul._combine_inverse(x*I*y, y*I) == x
    assert Mul._combine_inverse(oo*I*y, y*I) is oo
    assert Mul._combine_inverse(oo*I*y, oo*I) == y
    assert Mul._combine_inverse(oo*I*y, oo*I) == y
    assert Mul._combine_inverse(oo*y, -oo) == -y
    assert Mul._combine_inverse(-oo*y, oo) == -y
    assert Mul._combine_inverse((1-exp(x/y)),(exp(x/y)-1)) == -1
    assert Add._combine_inverse(oo, oo) is S.Zero
    assert Add._combine_inverse(oo*I, oo*I) is S.Zero
    assert Add._combine_inverse(x*oo, x*oo) is S.Zero
    assert Add._combine_inverse(-x*oo, -x*oo) is S.Zero
    assert Add._combine_inverse((x - oo)*(x + oo), -oo)

