
def test_exp__as_base_exp():
    assert exp(x).as_base_exp() == (E, x)
    assert exp(2*x).as_base_exp() == (E, 2*x)
    assert exp(x*y).as_base_exp() == (E, x*y)
    assert exp(-x).as_base_exp() == (E, -x)

    # Pow( *expr.as_base_exp() ) == expr    invariant should hold
    assert E**x == exp(x)
    assert E**(2*x) == exp(2*x)
    assert E**(x*y) == exp(x*y)

    assert exp(x).base is S.Exp1
    assert exp(x).exp == x

