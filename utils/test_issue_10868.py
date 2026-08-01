
def test_issue_10868():
    assert limit(log(x) + asech(x), x, 0, '+') == log(2)
    assert limit(log(x) + asech(x), x, 0, '-') == log(2) + 2*I*pi
    raises(ValueError, lambda: limit(log(x) + asech(x), x, 0, '+-'))
    assert limit(log(x) + asech(x), x, oo) == oo
    assert limit(log(x) + acsch(x), x, 0, '+') == log(2)
    assert limit(log(x) + acsch(x), x, 0, '-') == -oo
    raises(ValueError, lambda: limit(log(x) + acsch(x), x, 0, '+-'))
    assert limit(log(x) + acsch(x), x, oo) == oo

