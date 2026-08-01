
def test_given_sample():
    X = Die('X', 6)
    scipy = import_module('scipy')
    if not scipy:
        skip('Scipy is not installed. Abort tests')
    assert sample(X, X > 5) == 6

