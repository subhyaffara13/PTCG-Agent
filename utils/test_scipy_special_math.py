
def test_scipy_special_math():
    if not scipy:
        skip("scipy not installed")

    cm1 = lambdify((x,), cosm1(x), modules='scipy')
    assert abs(cm1(1e-20) + 5e-41) < 1e-200

    have_scipy_1_10plus = tuple(map(int, scipy.version.version.split('.')[:2])) >= (1, 10)

    if have_scipy_1_10plus:
        cm2 = lambdify((x, y), powm1(x, y), modules='scipy')
        assert abs(cm2(1.2, 1e-9) - 1.82321557e-10)  < 1e-17

