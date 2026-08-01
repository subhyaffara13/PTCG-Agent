
def test_aesara_function_bad_kwarg():
    """
    Passing an unknown keyword argument to aesara_function() should raise an
    exception.
    """
    raises(Exception, lambda : aesara_function_([x], [x+1], foobar=3))

