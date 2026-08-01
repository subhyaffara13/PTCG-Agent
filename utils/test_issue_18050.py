
def test_issue_18050():
    assert imageset(Lambda(x, I*x + 1), S.Integers
        ) == ImageSet(Lambda(x, I*x + 1), S.Integers)
    assert imageset(Lambda(x, 3*I*x + 4 + 8*I), S.Integers
        ) == ImageSet(Lambda(x, 3*I*x + 4 + 2*I), S.Integers)
    # no 'Mod' for next 2 tests:
    assert imageset(Lambda(x, 2*x + 3*I), S.Integers
        ) == ImageSet(Lambda(x, 2*x + 3*I), S.Integers)
    r = Symbol('r', positive=True)
    assert imageset(Lambda(x, r*x + 10), S.Integers
        ) == ImageSet(Lambda(x, r*x + 10), S.Integers)
    # reduce real part:
    assert imageset(Lambda(x, 3*x + 8 + 5*I), S.Integers
        ) == ImageSet(Lambda(x, 3*x + 2 + 5*I), S.Integers)

