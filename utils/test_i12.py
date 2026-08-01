
def test_I12():
    # This should fail or return nan or something.
    res = diff((tan(x)**2 + 1 - cos(x)**-2) / (sin(x)**2 + cos(x)**2 - 1), x)
    assert res is nan # trigsimp(res) gives nan

