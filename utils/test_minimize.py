
def test_minimize():
    def key(x: int) -> int:
        return -x

    rl = minimize(inc, dec)
    assert rl(4) == 3

    rl = minimize(inc, dec, objective=key)
    assert rl(4) == 5

