
def test_is_rational_function():
    assert Integer(1).is_rational_function() is True
    assert Integer(1).is_rational_function(x) is True

    assert Rational(17, 54).is_rational_function() is True
    assert Rational(17, 54).is_rational_function(x) is True

    assert (12/x).is_rational_function() is True
    assert (12/x).is_rational_function(x) is True

    assert (x/y).is_rational_function() is True
    assert (x/y).is_rational_function(x) is True
    assert (x/y).is_rational_function(x, y) is True

    assert (x**2 + 1/x/y).is_rational_function() is True
    assert (x**2 + 1/x/y).is_rational_function(x) is True
    assert (x**2 + 1/x/y).is_rational_function(x, y) is True

    assert (sin(y)/x).is_rational_function() is False
    assert (sin(y)/x).is_rational_function(y) is False
    assert (sin(y)/x).is_rational_function(x) is True
    assert (sin(y)/x).is_rational_function(x, y) is False

    for i in _illegal:
        assert not i.is_rational_function()
        for d in (1, x):
            assert not (i/d).is_rational_function()

