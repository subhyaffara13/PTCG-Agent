
def test_issue_16877():
    assert dumeq(nonlinsolve([x - 1, sin(y)], x, y),
                 FiniteSet((1, ImageSet(Lambda(n, 2*n*pi), S.Integers)),
                           (1, ImageSet(Lambda(n, 2*n*pi + pi), S.Integers))))

