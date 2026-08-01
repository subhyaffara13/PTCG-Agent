
def test_sample_iter():

    X = Normal('X',0,1)
    Y = DiscreteUniform('Y', [1, 2, 7])
    Z = Poisson('Z', 2)

    scipy = import_module('scipy')
    if not scipy:
        skip('Scipy is not installed. Abort tests')
    expr = X**2 + 3
    iterator = sample_iter(expr)

    expr2 = Y**2 + 5*Y + 4
    iterator2 = sample_iter(expr2)

    expr3 = Z**3 + 4
    iterator3 = sample_iter(expr3)

    def is_iterator(obj):
        if (
            hasattr(obj, '__iter__') and
            (hasattr(obj, 'next') or
            hasattr(obj, '__next__')) and
            callable(obj.__iter__) and
            obj.__iter__() is obj
           ):
            return True
        else:
            return False
    assert is_iterator(iterator)
    assert is_iterator(iterator2)
    assert is_iterator(iterator3)

