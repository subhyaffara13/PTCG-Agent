
def test_issue_19050():
    # test_issue_19050 --> TypeError removed
    assert dumeq(nonlinsolve([x + y, sin(y)], [x, y]),
        FiniteSet((ImageSet(Lambda(n, -2*n*pi), S.Integers), ImageSet(Lambda(n, 2*n*pi), S.Integers)),\
             (ImageSet(Lambda(n, -2*n*pi - pi), S.Integers), ImageSet(Lambda(n, 2*n*pi + pi), S.Integers))))
    assert dumeq(nonlinsolve([x + y, sin(y) + cos(y)], [x, y]),
        FiniteSet((ImageSet(Lambda(n, -2*n*pi - 3*pi/4), S.Integers), ImageSet(Lambda(n, 2*n*pi + 3*pi/4), S.Integers)), \
            (ImageSet(Lambda(n, -2*n*pi - 7*pi/4), S.Integers), ImageSet(Lambda(n, 2*n*pi + 7*pi/4), S.Integers))))

