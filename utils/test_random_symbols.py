
def test_random_symbols():
    X, Y = Normal('X', 0, 1), Normal('Y', 0, 1)

    assert set(random_symbols(2*X + 1)) == {X}
    assert set(random_symbols(2*X + Y)) == {X, Y}
    assert set(random_symbols(2*X + Y.symbol)) == {X}
    assert set(random_symbols(2)) == set()

