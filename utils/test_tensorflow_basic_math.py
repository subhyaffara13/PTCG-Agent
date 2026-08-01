
def test_tensorflow_basic_math():
    if not tensorflow:
        skip("tensorflow not installed.")
    expr = Max(sin(x), Abs(1/(x+2)))
    func = lambdify(x, expr, modules="tensorflow")

    with tensorflow.compat.v1.Session() as s:
        a = tensorflow.constant(0, dtype=tensorflow.float32)
        assert func(a).eval(session=s) == 0.5

