import re

def test_tensorflow_complexes():
    if not tensorflow:
        skip("tensorflow not installed")

    func1 = lambdify(x, re(x), modules="tensorflow")
    func2 = lambdify(x, im(x), modules="tensorflow")
    func3 = lambdify(x, Abs(x), modules="tensorflow")
    func4 = lambdify(x, arg(x), modules="tensorflow")

    with tensorflow.compat.v1.Session() as s:
        # For versions before
        # https://github.com/tensorflow/tensorflow/issues/30029
        # resolved, using Python numeric types may not work
        a = tensorflow.constant(1+2j)
        assert func1(a).eval(session=s) == 1
        assert func2(a).eval(session=s) == 2

        tensorflow_result = func3(a).eval(session=s)
        sympy_result = Abs(1 + 2j).evalf()
        assert abs(tensorflow_result-sympy_result) < 10**-6

        tensorflow_result = func4(a).eval(session=s)
        sympy_result = arg(1 + 2j).evalf()
        assert abs(tensorflow_result-sympy_result) < 10**-6


def test_tensorflow_complexes():
    assert tensorflow_code(re(x)) == "tensorflow.math.real(x)"
    assert tensorflow_code(im(x)) == "tensorflow.math.imag(x)"
    assert tensorflow_code(arg(x)) == "tensorflow.math.angle(x)"

