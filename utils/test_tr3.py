
def test_TR3():
    assert TR3(cos(y - x*(y - x))) == cos(x*(x - y) + y)
    assert cos(pi/2 + x) == -sin(x)
    assert cos(30*pi/2 + x) == -cos(x)

    for f in (cos, sin, tan, cot, csc, sec):
        i = f(pi*Rational(3, 7))
        j = TR3(i)
        assert verify_numerically(i, j) and i.func != j.func

    with evaluate(False):
        eq = cos(9*pi/22)
    assert eq.has(9*pi) and TR3(eq) == sin(pi/11)

