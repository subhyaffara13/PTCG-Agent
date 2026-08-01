
def test_descent():

    u = ([(13, 23), (3, -11), (41, -113), (91, -3), (1, 1), (1, -1), (17, 13), (123689, 1), (19, -570)])
    for a, b in u:
        w, x, y = descent(a, b)
        assert a*x**2 + b*y**2 == w**2
    # the docstring warns against bad input, so these are expected results
    # - can't both be negative
    raises(TypeError, lambda: descent(-1, -3))
    # A can't be zero unless B != 1
    raises(ZeroDivisionError, lambda: descent(0, 3))
    # supposed to be square-free
    raises(TypeError, lambda: descent(4, 3))

