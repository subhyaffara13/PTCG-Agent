
def test_partial_simp():
    # First test that hypergeometric function formulae work.
    a, b, c, d, e = (randcplx() for _ in range(5))
    for func in [Hyper_Function([a, b, c], [d, e]),
            Hyper_Function([], [a, b, c, d, e])]:
        f = build_hypergeometric_formula(func)
        z = f.z
        assert f.closed_form == func(z)
        deriv1 = f.B.diff(z)*z
        deriv2 = f.M*f.B
        for func1, func2 in zip(deriv1, deriv2):
            assert tn(func1, func2, z)

    # Now test that formulae are partially simplified.
    a, b, z = symbols('a b z')
    assert hyperexpand(hyper([3, a], [1, b], z)) == \
        (-a*b/2 + a*z/2 + 2*a)*hyper([a + 1], [b], z) \
        + (a*b/2 - 2*a + 1)*hyper([a], [b], z)
    assert tn(
        hyperexpand(hyper([3, d], [1, e], z)), hyper([3, d], [1, e], z), z)
    assert hyperexpand(hyper([3], [1, a, b], z)) == \
        hyper((), (a, b), z) \
        + z*hyper((), (a + 1, b), z)/(2*a) \
        - z*(b - 4)*hyper((), (a + 1, b + 1), z)/(2*a*b)
    assert tn(
        hyperexpand(hyper([3], [1, d, e], z)), hyper([3], [1, d, e], z), z)

