
def test_tensorflow_math():
    if not tf:
        skip("TensorFlow not installed")

    expr = Abs(x)
    assert tensorflow_code(expr) == "tensorflow.math.abs(x)"
    _compare_tensorflow_scalar((x,), expr)

    expr = sign(x)
    assert tensorflow_code(expr) == "tensorflow.math.sign(x)"
    _compare_tensorflow_scalar((x,), expr)

    expr = ceiling(x)
    assert tensorflow_code(expr) == "tensorflow.math.ceil(x)"
    _compare_tensorflow_scalar((x,), expr, rng=lambda: random.random())

    expr = floor(x)
    assert tensorflow_code(expr) == "tensorflow.math.floor(x)"
    _compare_tensorflow_scalar((x,), expr, rng=lambda: random.random())

    expr = exp(x)
    assert tensorflow_code(expr) == "tensorflow.math.exp(x)"
    _compare_tensorflow_scalar((x,), expr, rng=lambda: random.random())

    expr = sqrt(x)
    assert tensorflow_code(expr) == "tensorflow.math.sqrt(x)"
    _compare_tensorflow_scalar((x,), expr, rng=lambda: random.random())

    expr = x ** 4
    assert tensorflow_code(expr) == "tensorflow.math.pow(x, 4)"
    _compare_tensorflow_scalar((x,), expr, rng=lambda: random.random())

    expr = cos(x)
    assert tensorflow_code(expr) == "tensorflow.math.cos(x)"
    _compare_tensorflow_scalar((x,), expr, rng=lambda: random.random())

    expr = acos(x)
    assert tensorflow_code(expr) == "tensorflow.math.acos(x)"
    _compare_tensorflow_scalar((x,), expr, rng=lambda: random.uniform(0, 0.95))

    expr = sin(x)
    assert tensorflow_code(expr) == "tensorflow.math.sin(x)"
    _compare_tensorflow_scalar((x,), expr, rng=lambda: random.random())

    expr = asin(x)
    assert tensorflow_code(expr) == "tensorflow.math.asin(x)"
    _compare_tensorflow_scalar((x,), expr, rng=lambda: random.random())

    expr = tan(x)
    assert tensorflow_code(expr) == "tensorflow.math.tan(x)"
    _compare_tensorflow_scalar((x,), expr, rng=lambda: random.random())

    expr = atan(x)
    assert tensorflow_code(expr) == "tensorflow.math.atan(x)"
    _compare_tensorflow_scalar((x,), expr, rng=lambda: random.random())

    expr = atan2(y, x)
    assert tensorflow_code(expr) == "tensorflow.math.atan2(y, x)"
    _compare_tensorflow_scalar((y, x), expr, rng=lambda: random.random())

    expr = cosh(x)
    assert tensorflow_code(expr) == "tensorflow.math.cosh(x)"
    _compare_tensorflow_scalar((x,), expr, rng=lambda: random.random())

    expr = acosh(x)
    assert tensorflow_code(expr) == "tensorflow.math.acosh(x)"
    _compare_tensorflow_scalar((x,), expr, rng=lambda: random.uniform(1, 2))

    expr = sinh(x)
    assert tensorflow_code(expr) == "tensorflow.math.sinh(x)"
    _compare_tensorflow_scalar((x,), expr, rng=lambda: random.uniform(1, 2))

    expr = asinh(x)
    assert tensorflow_code(expr) == "tensorflow.math.asinh(x)"
    _compare_tensorflow_scalar((x,), expr, rng=lambda: random.uniform(1, 2))

    expr = tanh(x)
    assert tensorflow_code(expr) == "tensorflow.math.tanh(x)"
    _compare_tensorflow_scalar((x,), expr, rng=lambda: random.uniform(1, 2))

    expr = atanh(x)
    assert tensorflow_code(expr) == "tensorflow.math.atanh(x)"
    _compare_tensorflow_scalar(
        (x,), expr, rng=lambda: random.uniform(-.5, .5))

    expr = erf(x)
    assert tensorflow_code(expr) == "tensorflow.math.erf(x)"
    _compare_tensorflow_scalar(
        (x,), expr, rng=lambda: random.random())

    expr = loggamma(x)
    assert tensorflow_code(expr) == "tensorflow.math.lgamma(x)"
    _compare_tensorflow_scalar(
        (x,), expr, rng=lambda: random.random())

