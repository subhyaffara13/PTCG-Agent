
def test_integrate_SingularityFunction():
    in_1 = SingularityFunction(x, a, 3) + SingularityFunction(x, 5, -1)
    out_1 = SingularityFunction(x, a, 4)/4 + SingularityFunction(x, 5, 0)
    assert integrate(in_1, x) == out_1

    in_2 = 10*SingularityFunction(x, 4, 0) - 5*SingularityFunction(x, -6, -2)
    out_2 = 10*SingularityFunction(x, 4, 1) - 5*SingularityFunction(x, -6, -1)
    assert integrate(in_2, x) == out_2

    in_3 = 2*x**2*y -10*SingularityFunction(x, -4, 7) - 2*SingularityFunction(y, 10, -2)
    out_3_1 = 2*x**3*y/3 - 2*x*SingularityFunction(y, 10, -2) - 5*SingularityFunction(x, -4, 8)/4
    out_3_2 = x**2*y**2 - 10*y*SingularityFunction(x, -4, 7) - 2*SingularityFunction(y, 10, -1)
    assert integrate(in_3, x) == out_3_1
    assert integrate(in_3, y) == out_3_2

    assert unchanged(Integral, in_3, (x,))
    assert Integral(in_3, x) == Integral(in_3, (x,))
    assert Integral(in_3, x).doit() == out_3_1

    in_4 = 10*SingularityFunction(x, -4, 7) - 2*SingularityFunction(x, 10, -2)
    out_4 = 5*SingularityFunction(x, -4, 8)/4 - 2*SingularityFunction(x, 10, -1)
    assert integrate(in_4, (x, -oo, x)) == out_4

    assert integrate(SingularityFunction(x, 5, -1), x) == SingularityFunction(x, 5, 0)
    assert integrate(SingularityFunction(x, 0, -1), (x, -oo, oo)) == 1
    assert integrate(5*SingularityFunction(x, 5, -1), (x, -oo, oo)) == 5
    assert integrate(SingularityFunction(x, 5, -1) * f(x), (x, -oo, oo)) == f(5)

