
def test_oddness_in_ternary_integer_product_with_even():
    x = Symbol('x', integer=True)
    y = Symbol('y', integer=True)
    m = Symbol('m', even=True)
    assert (x*y*(y + m)).is_odd is None


def test_oddness_in_ternary_integer_product_with_even():
    assert ask(Q.odd(x*y*(y + z)), Q.integer(x) & Q.integer(y) & Q.even(z)) is None

