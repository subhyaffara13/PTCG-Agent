
def test_quadratic_non_perfect_square():
    # B**2 - 4*A*C is not a perfect square
    # Used check_solutions() since the solutions are complex expressions involving
    # square roots and exponents
    assert check_solutions(x**2 - 2*x - 5*y**2)
    assert check_solutions(3*x**2 - 2*y**2 - 2*x - 2*y)
    assert check_solutions(x**2 - x*y - y**2 - 3*y)
    assert check_solutions(x**2 - 9*y**2 - 2*x - 6*y)
    assert BinaryQuadratic(x**2 + y**2 + 2*x + 2*y + 2).solve() == {(-1, -1)}

