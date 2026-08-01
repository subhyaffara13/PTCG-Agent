
def test_Symbol_two_assumptions():
    x = Symbol('x', negative=0, integer=1)
    # order could vary
    s1 = "Symbol('x', integer=True, negative=False)"
    s2 = "Symbol('x', negative=False, integer=True)"
    assert srepr(x) in (s1, s2)
    assert eval(srepr(x), ENV) == x

