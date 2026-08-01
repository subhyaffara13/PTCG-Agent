
def test_issue_16876():
    assert dumeq(nonlinsolve([sin(x), 2*x - 4*y], x, y),
                 FiniteSet((ImageSet(Lambda(n, 2*n*pi), S.Integers),
                            ImageSet(Lambda(n, n*pi), S.Integers)),
                           (ImageSet(Lambda(n, 2*n*pi + pi), S.Integers),
                            ImageSet(Lambda(n, n*pi + pi/2), S.Integers))))

