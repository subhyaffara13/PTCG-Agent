
def test_series_of_Subs():
    from sympy.abc import z

    subs1 = Subs(sin(x), x, y)
    subs2 = Subs(sin(x) * cos(z), x, y)
    subs3 = Subs(sin(x * z), (x, z), (y, x))

    assert subs1.series(x) == subs1
    subs1_series = (Subs(x, x, y) + Subs(-x**3/6, x, y) +
        Subs(x**5/120, x, y) + O(y**6))
    assert subs1.series() == subs1_series
    assert subs1.series(y) == subs1_series
    assert subs1.series(z) == subs1
    assert subs2.series(z) == (Subs(z**4*sin(x)/24, x, y) +
        Subs(-z**2*sin(x)/2, x, y) + Subs(sin(x), x, y) + O(z**6))
    assert subs3.series(x).doit() == subs3.doit().series(x)
    assert subs3.series(z).doit() == sin(x*y)

    raises(ValueError, lambda: Subs(x + 2*y, y, z).series())
    assert Subs(x + y, y, z).series(x).doit() == x + z

