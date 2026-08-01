
def test_rademacher():
    X = Rademacher('X')
    t = Symbol('t')

    assert E(X) == 0
    assert variance(X) == 1
    assert density(X)[-1] == S.Half
    assert density(X)[1] == S.Half
    assert characteristic_function(X)(t) == exp(I*t)/2 + exp(-I*t)/2
    assert moment_generating_function(X)(t) == exp(t) / 2 + exp(-t) / 2

