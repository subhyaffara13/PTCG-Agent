
def test_tensorflow_variables():
    if not tensorflow:
        skip("tensorflow not installed.")
    expr = Max(sin(x), Abs(1/(x+2)))
    func = lambdify(x, expr, modules="tensorflow")

    with tensorflow.compat.v1.Session() as s:
        a = tensorflow.Variable(0, dtype=tensorflow.float32)
        s.run(a.initializer)
        assert func(a).eval(session=s, feed_dict={a: 0}) == 0.5

