
def test_probability_unevaluated():
    T = Normal('T', 30, 3)
    with ignore_warnings(UserWarning): ### TODO: Restore tests once warnings are removed
        assert type(P(T > 33, evaluate=False)) == Probability

