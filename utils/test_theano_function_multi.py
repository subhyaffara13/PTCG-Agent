
def test_theano_function_multi():
    """ Test theano_function() with multiple outputs. """
    f = theano_function_([x, y], [x+y, x-y])
    o1, o2 = f(2, 3)
    assert o1 == 5
    assert o2 == -1

