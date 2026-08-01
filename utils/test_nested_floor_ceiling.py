
def test_nested_floor_ceiling():
    assert floor(-floor(ceiling(x**3)/y)) == -floor(ceiling(x**3)/y)
    assert ceiling(-floor(ceiling(x**3)/y)) == -floor(ceiling(x**3)/y)
    assert floor(ceiling(-floor(x**Rational(7, 2)/y))) == -floor(x**Rational(7, 2)/y)
    assert -ceiling(-ceiling(floor(x)/y)) == ceiling(floor(x)/y)

