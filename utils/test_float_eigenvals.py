
def test_float_eigenvals():
    m = Matrix([[1, .6, .6], [.6, .9, .9], [.9, .6, .6]])
    evals = [
        Rational(5, 4) - sqrt(385)/20,
        sqrt(385)/20 + Rational(5, 4),
        S.Zero]

    n_evals = m.eigenvals(rational=True, multiple=True)
    n_evals = sorted(n_evals)
    s_evals = [x.evalf() for x in evals]
    s_evals = sorted(s_evals)

    for x, y in zip(n_evals, s_evals):
        assert abs(x-y) < 10**-9

