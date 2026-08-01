
def test_spherical_bessel():
    if numpy and not scipy:
        skip("scipy not installed.")
    test_point = 4.2 #randomly selected
    x = symbols("x")
    jtest = jn(2, x)
    assert abs(lambdify(x,jtest)(test_point) -
            jtest.subs(x,test_point).evalf()) < 1e-8
    ytest = yn(2, x)
    assert abs(lambdify(x,ytest)(test_point) -
            ytest.subs(x,test_point).evalf()) < 1e-8

