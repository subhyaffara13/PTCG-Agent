
def test_integrate_function_of_square_over_negatives():
    assert integrate(exp(-x**2), (x,-5,0), meijerg=True) == sqrt(pi)/2 * erf(5)

