
def test_theano_function_bad_kwarg():
    """
    Passing an unknown keyword argument to theano_function() should raise an
    exception.
    """
    raises(Exception, lambda : theano_function_([x], [x+1], foobar=3))

