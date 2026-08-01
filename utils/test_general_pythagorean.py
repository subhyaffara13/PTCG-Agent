
def test_general_pythagorean():
    from sympy.abc import a, b, c, d, e

    assert check_solutions(a**2 + b**2 + c**2 - d**2)
    assert check_solutions(a**2 + 4*b**2 + 4*c**2 - d**2)
    assert check_solutions(9*a**2 + 4*b**2 + 4*c**2 - d**2)
    assert check_solutions(9*a**2 + 4*b**2 - 25*d**2 + 4*c**2 )
    assert check_solutions(9*a**2 - 16*d**2 + 4*b**2 + 4*c**2)
    assert check_solutions(-e**2 + 9*a**2 + 4*b**2 + 4*c**2 + 25*d**2)
    assert check_solutions(16*a**2 - b**2 + 9*c**2 + d**2 + 25*e**2)

    assert GeneralPythagorean(a**2 + b**2 + c**2 - d**2).solve(parameters=[x, y, z]) == \
           {(x**2 + y**2 - z**2, 2*x*z, 2*y*z, x**2 + y**2 + z**2)}

