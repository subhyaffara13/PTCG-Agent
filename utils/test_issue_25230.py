
def test_issue_25230():
    a = Symbol('a', real = True)
    b = Symbol('b', positive = True)
    c = Symbol('c', negative = True)
    n = Symbol('n', integer = True)
    raises(NotImplementedError, lambda: limit(Mod(x, a), x, a))
    assert limit(Mod(x, b), x, n*b, '+') == 0
    assert limit(Mod(x, b), x, n*b, '-') == b
    assert limit(Mod(x, c), x, n*c, '+') == c
    assert limit(Mod(x, c), x, n*c, '-') == 0


def test_issue_25230():
    a = Symbol('a', real = True)
    b = Symbol('b', positive = True)
    c = Symbol('c', negative = True)
    raises(NotImplementedError, lambda: floor(x/a).as_leading_term(x, cdir = 1))
    raises(NotImplementedError, lambda: ceiling(x/a).as_leading_term(x, cdir = 1))
    assert floor(x/b).as_leading_term(x, cdir = 1) == 0
    assert floor(x/b).as_leading_term(x, cdir = -1) == -1
    assert floor(x/c).as_leading_term(x, cdir = 1) == -1
    assert floor(x/c).as_leading_term(x, cdir = -1) == 0
    assert ceiling(x/b).as_leading_term(x, cdir = 1) == 1
    assert ceiling(x/b).as_leading_term(x, cdir = -1) == 0
    assert ceiling(x/c).as_leading_term(x, cdir = 1) == 0
    assert ceiling(x/c).as_leading_term(x, cdir = -1) == 1

