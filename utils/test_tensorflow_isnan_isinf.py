
def test_tensorflow_isnan_isinf():
    if not tf:
        skip("TensorFlow not installed")

    # Test for isnan
    x = symbols("x")
    # Return 0 if x is of nan value, and 1 otherwise
    expression = Piecewise((0.0, isnan(x)), (1.0, True))
    printed_code = tensorflow_code(expression)
    expected_printed_code = "tensorflow.where(tensorflow.math.is_nan(x), 0.0, 1.0)"
    assert tensorflow_code(expression) == expected_printed_code, f"Incorrect printed result {printed_code}, expected {expected_printed_code}"
    for _input, _expected in [(float('nan'), 0.0), (float('inf'), 1.0), (float('-inf'), 1.0), (1.0, 1.0)]:
        _output = lambdify((x), expression, modules="tensorflow")(x=tf.constant([_input]))
        assert (_output == _expected).numpy().all()

    # Test for isinf
    x = symbols("x")
    # Return 0 if x is of nan value, and 1 otherwise
    expression = Piecewise((0.0, isinf(x)), (1.0, True))
    printed_code = tensorflow_code(expression)
    expected_printed_code = "tensorflow.where(tensorflow.math.is_inf(x), 0.0, 1.0)"
    assert tensorflow_code(expression) == expected_printed_code, f"Incorrect printed result {printed_code}, expected {expected_printed_code}"
    for _input, _expected in [(float('inf'), 0.0), (float('-inf'), 0.0), (float('nan'), 1.0), (1.0, 1.0)]:
        _output = lambdify((x), expression, modules="tensorflow")(x=tf.constant([_input]))
        assert (_output == _expected).numpy().all()

