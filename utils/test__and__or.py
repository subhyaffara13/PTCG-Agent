
def test_And_Or():
    # precedence relations between logical operators, ...
    assert precedence(x & y) > precedence(x | y)
    assert precedence(~y) > precedence(x & y)
    # ... and with other operators (cfr. other programming languages)
    assert precedence(x + y) > precedence(x | y)
    assert precedence(x + y) > precedence(x & y)
    assert precedence(x*y) > precedence(x | y)
    assert precedence(x*y) > precedence(x & y)
    assert precedence(~y) > precedence(x*y)
    assert precedence(~y) > precedence(x - y)
    # double checks
    assert precedence(x & y) == PRECEDENCE["And"]
    assert precedence(x | y) == PRECEDENCE["Or"]
    assert precedence(~y) == PRECEDENCE["Not"]

