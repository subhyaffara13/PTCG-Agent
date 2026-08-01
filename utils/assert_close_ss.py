
def assert_close_ss(sol1, sol2):
    """Test solutions with floats from solveset are close"""
    sol1 = sympify(sol1)
    sol2 = sympify(sol2)
    assert isinstance(sol1, FiniteSet)
    assert isinstance(sol2, FiniteSet)
    assert len(sol1) == len(sol2)
    assert all(isclose(v1, v2) for v1, v2 in zip(sol1, sol2))

