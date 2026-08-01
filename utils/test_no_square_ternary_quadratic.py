
def test_no_square_ternary_quadratic():
    assert check_solutions(2*x*y + y*z - 3*x*z)
    assert check_solutions(189*x*y - 345*y*z - 12*x*z)
    assert check_solutions(23*x*y + 34*y*z)
    assert check_solutions(x*y + y*z + z*x)
    assert check_solutions(23*x*y + 23*y*z + 23*x*z)

