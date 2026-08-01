
def test_tensorflow_Derivative():
    expr = Derivative(sin(x), x)
    assert tensorflow_code(expr) == \
        "tensorflow.gradients(tensorflow.math.sin(x), x)[0]"

