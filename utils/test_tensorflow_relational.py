
def test_tensorflow_relational():
    if not tensorflow:
        skip("tensorflow not installed.")
    expr = x >= 0
    func = lambdify(x, expr, modules="tensorflow")

    with tensorflow.compat.v1.Session() as s:
        assert func(1).eval(session=s) == True


def test_tensorflow_relational():
    if not tf:
        skip("TensorFlow not installed")

    expr = Eq(x, y)
    assert tensorflow_code(expr) == "tensorflow.math.equal(x, y)"
    _compare_tensorflow_relational((x, y), expr)

    expr = Ne(x, y)
    assert tensorflow_code(expr) == "tensorflow.math.not_equal(x, y)"
    _compare_tensorflow_relational((x, y), expr)

    expr = Ge(x, y)
    assert tensorflow_code(expr) == "tensorflow.math.greater_equal(x, y)"
    _compare_tensorflow_relational((x, y), expr)

    expr = Gt(x, y)
    assert tensorflow_code(expr) == "tensorflow.math.greater(x, y)"
    _compare_tensorflow_relational((x, y), expr)

    expr = Le(x, y)
    assert tensorflow_code(expr) == "tensorflow.math.less_equal(x, y)"
    _compare_tensorflow_relational((x, y), expr)

    expr = Lt(x, y)
    assert tensorflow_code(expr) == "tensorflow.math.less(x, y)"
    _compare_tensorflow_relational((x, y), expr)

