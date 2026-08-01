
def test_trig_nonelementary_integrals():
    x = Symbol('x')
    assert integrate((1 + sin(x))/x, x) == log(x) + Si(x)
    # next one comes out as log(x) + log(x**2)/2 + Ci(x)
    # so not hardcoding this log ugliness
    assert integrate((cos(x) + 2)/x, x).has(Ci)

