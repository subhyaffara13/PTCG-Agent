
def test_integrate_poly_accurately():
    y = Symbol('y')
    assert integrate(x*sin(y), x) == x**2*sin(y)/2

    # when passed to risch_norman, this will be a CPU hog, so this really
    # checks, that integrated function is recognized as polynomial
    assert integrate(x**1000*sin(y), x) == x**1001*sin(y)/1001

