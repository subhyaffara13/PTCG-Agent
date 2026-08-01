
def test_Limits_simple_3b():
    h = Symbol("h")
    assert limit(((x + h)**3 - x**3)/h, h, 0) == 3*x**2  # 197
    assert limit((1/(1 - x) - 3/(1 - x**3)), x, 1) == -1  # 198
    assert limit((sqrt(1 + x) - 1)/(root3(1 + x) - 1), x, 0) == Rational(3)/2  # Primer 4
    assert limit((sqrt(x) - 1)/(x - 1), x, 1) == Rational(1)/2  # 199
    assert limit((sqrt(x) - 8)/(root3(x) - 4), x, 64) == 3  # 200
    assert limit((root3(x) - 1)/(root4(x) - 1), x, 1) == Rational(4)/3  # 201
    assert limit(
        (root3(x**2) - 2*root3(x) + 1)/(x - 1)**2, x, 1) == Rational(1)/9  # 202

