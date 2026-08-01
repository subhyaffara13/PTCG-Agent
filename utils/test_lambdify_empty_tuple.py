
def test_lambdify_empty_tuple():
    a = symbols("a")
    expr = ((), (a,))
    f = lambdify(a, expr)
    result = f(1)
    assert result == ((), (1,)), "Lambdify did not handle the empty tuple correctly."

