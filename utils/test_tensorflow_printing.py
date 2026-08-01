
def test_tensorflow_printing():
    assert tensorflow_code(eye(3)) == \
        "tensorflow.constant([[1, 0, 0], [0, 1, 0], [0, 0, 1]])"

    expr = Matrix([[x, sin(y)], [exp(z), -t]])
    assert tensorflow_code(expr) == \
        "tensorflow.Variable(" \
            "[[x, tensorflow.math.sin(y)]," \
            " [tensorflow.math.exp(z), -t]])"

