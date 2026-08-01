
def test_Limits_simple_1():
    assert limit((x + 1)*(x + 2)*(x + 3)/x**3, x, oo) == 1  # 172
    assert limit(sqrt(x + 1) - sqrt(x), x, oo) == 0  # 179
    assert limit((2*x - 3)*(3*x + 5)*(4*x - 6)/(3*x**3 + x - 1), x, oo) == 8  # Primjer 1
    assert limit(x/root3(x**3 + 10), x, oo) == 1  # Primjer 2
    assert limit((x + 1)**2/(x**2 + 1), x, oo) == 1  # 181

