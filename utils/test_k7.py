
def test_K7():
    y = symbols('y', real=True, negative=False)
    expr = sqrt(x*y*abs(z)**2)/(sqrt(x)*abs(z))
    sexpr = simplify(expr)
    assert sexpr == sqrt(y)

