
def test_solver_flags():
    root = solve(x**5 + x**2 - x - 1, cubics=False)
    rad = solve(x**5 + x**2 - x - 1, cubics=True)
    assert root != rad

