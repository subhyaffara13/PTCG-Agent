
def test_term_factors():
    assert list(_term_factors(3**x - 2)) == [-2, 3**x]
    expr = 4**(x + 1) + 4**(x + 2) + 4**(x - 1) - 3**(x + 2) - 3**(x + 3)
    assert set(_term_factors(expr)) == {
        3**(x + 2), 4**(x + 2), 3**(x + 3), 4**(x - 1), -1, 4**(x + 1)}

