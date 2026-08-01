
def test_tensorflow_multi_min():
    if not tensorflow:
        skip("tensorflow not installed.")
    expr = Min(x, -x, x**2)
    func = lambdify(x, expr, modules="tensorflow")

    with tensorflow.compat.v1.Session() as s:
        assert func(-2).eval(session=s) == -2

