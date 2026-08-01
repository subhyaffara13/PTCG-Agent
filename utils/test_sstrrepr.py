
def test_sstrrepr():
    assert sstr('abc') == 'abc'
    assert sstrrepr('abc') == "'abc'"

    e = ['a', 'b', 'c', x]
    assert sstr(e) == "[a, b, c, x]"
    assert sstrrepr(e) == "['a', 'b', 'c', x]"

