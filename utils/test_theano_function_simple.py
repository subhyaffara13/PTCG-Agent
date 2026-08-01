
def test_theano_function_simple():
    """ Test theano_function() with single output. """
    f = theano_function_([x, y], [x+y])
    assert f(2, 3) == 5

