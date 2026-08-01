
def test_bernoulli_CompoundDist():
    X = Beta('X', 1, 2)
    Y = Bernoulli('Y', X)
    assert density(Y).dict == {0: S(2)/3, 1: S(1)/3}
    assert E(Y) == P(Eq(Y, 1)) == S(1)/3
    assert variance(Y) == S(2)/9
    assert cdf(Y) == {0: S(2)/3, 1: 1}

    # test issue 8128
    a = Bernoulli('a', S(1)/2)
    b = Bernoulli('b', a)
    assert density(b).dict == {0: S(1)/2, 1: S(1)/2}
    assert P(b > 0.5) == S(1)/2

    X = Uniform('X', 0, 1)
    Y = Bernoulli('Y', X)
    assert E(Y) == S(1)/2
    assert P(Eq(Y, 1)) == E(Y)

