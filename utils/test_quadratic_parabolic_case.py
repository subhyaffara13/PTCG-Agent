
def test_quadratic_parabolic_case():
    # Parabolic case: B**2 - 4AC = 0
    assert check_solutions(8*x**2 - 24*x*y + 18*y**2 + 5*x + 7*y + 16)
    assert check_solutions(8*x**2 - 24*x*y + 18*y**2 + 6*x + 12*y - 6)
    assert check_solutions(8*x**2 + 24*x*y + 18*y**2 + 4*x + 6*y - 7)
    assert check_solutions(-4*x**2 + 4*x*y - y**2 + 2*x - 3)
    assert check_solutions(x**2 + 2*x*y + y**2 + 2*x + 2*y + 1)
    assert check_solutions(x**2 - 2*x*y + y**2 + 2*x + 2*y + 1)
    assert check_solutions(y**2 - 41*x + 40)

