
def test_23536_lambdify_cse_dummy():

    f = Function('x')(y)
    g = Function('w')(y)
    expr = z + (f**4 + g**5)*(f**3 + (g*f)**3)
    expr = expr.expand()
    eval_expr = lambdify(((f, g), z), expr, cse=True)
    ans = eval_expr((1.0, 2.0), 3.0)  # shouldn't raise NameError
    assert ans == 300.0  # not a list and value is 300

