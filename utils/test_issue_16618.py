
def test_issue_16618():
    eqn = [sin(x)*sin(y), cos(x)*cos(y) - 1]
    # nonlinsolve's answer is still suspicious since it contains only three
    # distinct Dummys instead of 4. (Both 'x' ImageSets share the same Dummy.)
    ans = FiniteSet((ImageSet(Lambda(n, 2*n*pi), S.Integers), ImageSet(Lambda(n, 2*n*pi), S.Integers)),
        (ImageSet(Lambda(n, 2*n*pi + pi), S.Integers), ImageSet(Lambda(n, 2*n*pi + pi), S.Integers)))
    sol = nonlinsolve(eqn, [x, y])

    for i0, j0 in zip(ordered(sol), ordered(ans)):
        assert len(i0) == len(j0) == 2
        assert all(a.dummy_eq(b) for a, b in zip(i0, j0))
    assert len(sol) == len(ans)

