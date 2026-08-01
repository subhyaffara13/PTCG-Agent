
def test_aesara_function_simple():
    """ Test aesara_function() with single output. """
    f = aesara_function_([x, y], [x+y])
    assert f(2, 3) == 5

