
def test_trivial_indices():
    x, y = symbols('x y')
    assert get_indices(x) == (set(), {})
    assert get_indices(x*y) == (set(), {})
    assert get_indices(x + y) == (set(), {})
    assert get_indices(x**y) == (set(), {})

