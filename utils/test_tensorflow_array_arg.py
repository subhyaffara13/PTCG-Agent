
def test_tensorflow_array_arg():
    # Test for issue 14655 (tensorflow part)
    if not tensorflow:
        skip("tensorflow not installed.")

    f = lambdify([[x, y]], x*x + y, 'tensorflow')

    with tensorflow.compat.v1.Session() as s:
        fcall = f(tensorflow.constant([2.0, 1.0]))
        assert fcall.eval(session=s) == 5.0

