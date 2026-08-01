
def test_expand_log():
    t = Symbol('t', positive=True)
    # after first expansion, -2*log(2) + log(4); then 0 after second
    assert expand(log(t**2) - log(t**2/4) - 2*log(2)) == 0
    assert expand_log(log(7*6)/log(6)) == 1 + log(7)/log(6)
    b = factorial(10)
    assert expand_log(log(7*b**4)/log(b)
        ) == 4 + log(7)/log(b)

