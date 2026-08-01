
def test_broadcast_size_error():
    mu = np.ones(3)
    sigma = np.ones((4, 3))
    size = (10, 4, 2)
    assert random.normal(mu, sigma, size=(5, 4, 3)).shape == (5, 4, 3)
    with pytest.raises(ValueError):
        random.normal(mu, sigma, size=size)
    with pytest.raises(ValueError):
        random.normal(mu, sigma, size=(1, 3))
    with pytest.raises(ValueError):
        random.normal(mu, sigma, size=(4, 1, 1))
    # 1 arg
    shape = np.ones((4, 3))
    with pytest.raises(ValueError):
        random.standard_gamma(shape, size=size)
    with pytest.raises(ValueError):
        random.standard_gamma(shape, size=(3,))
    with pytest.raises(ValueError):
        random.standard_gamma(shape, size=3)
    # Check out
    out = np.empty(size)
    with pytest.raises(ValueError):
        random.standard_gamma(shape, out=out)

    # 2 arg
    with pytest.raises(ValueError):
        random.binomial(1, [0.3, 0.7], size=(2, 1))
    with pytest.raises(ValueError):
        random.binomial([1, 2], 0.3, size=(2, 1))
    with pytest.raises(ValueError):
        random.binomial([1, 2], [0.3, 0.7], size=(2, 1))
    with pytest.raises(ValueError):
        random.multinomial([2, 2], [.3, .7], size=(2, 1))

    # 3 arg
    a = random.chisquare(5, size=3)
    b = random.chisquare(5, size=(4, 3))
    c = random.chisquare(5, size=(5, 4, 3))
    assert random.noncentral_f(a, b, c).shape == (5, 4, 3)
    with pytest.raises(ValueError, match=r"Output size \(6, 5, 1, 1\) is"):
        random.noncentral_f(a, b, c, size=(6, 5, 1, 1))


def test_broadcast_size_error():
    # GH-16833
    with pytest.raises(ValueError):
        random.binomial(1, [0.3, 0.7], size=(2, 1))
    with pytest.raises(ValueError):
        random.binomial([1, 2], 0.3, size=(2, 1))
    with pytest.raises(ValueError):
        random.binomial([1, 2], [0.3, 0.7], size=(2, 1))

