
def test_solve_decomposition():
    n = Dummy('n')

    f1 = exp(3*x) - 6*exp(2*x) + 11*exp(x) - 6
    f2 = sin(x)**2 - 2*sin(x) + 1
    f3 = sin(x)**2 - sin(x)
    f4 = sin(x + 1)
    f5 = exp(x + 2) - 1
    f6 = 1/log(x)
    f7 = 1/x

    s1 = ImageSet(Lambda(n, 2*n*pi), S.Integers)
    s2 = ImageSet(Lambda(n, 2*n*pi + pi), S.Integers)
    s3 = ImageSet(Lambda(n, 2*n*pi + pi/2), S.Integers)
    s4 = ImageSet(Lambda(n, 2*n*pi - 1), S.Integers)
    s5 = ImageSet(Lambda(n, 2*n*pi - 1 + pi), S.Integers)

    assert solve_decomposition(f1, x, S.Reals) == FiniteSet(0, log(2), log(3))
    assert dumeq(solve_decomposition(f2, x, S.Reals), s3)
    assert dumeq(solve_decomposition(f3, x, S.Reals), Union(s1, s2, s3))
    assert dumeq(solve_decomposition(f4, x, S.Reals), Union(s4, s5))
    assert solve_decomposition(f5, x, S.Reals) == FiniteSet(-2)
    assert solve_decomposition(f6, x, S.Reals) == S.EmptySet
    assert solve_decomposition(f7, x, S.Reals) == S.EmptySet
    assert solve_decomposition(x, x, Interval(1, 2)) == S.EmptySet

