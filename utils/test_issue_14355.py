
def test_issue_14355():
    assert limit(floor(sin(x)/x), x, 0, '+') == 0
    assert limit(floor(sin(x)/x), x, 0, '-') == 0
    # test comment https://github.com/sympy/sympy/issues/14355#issuecomment-372121314
    assert limit(floor(-tan(x)/x), x, 0, '+') == -2
    assert limit(floor(-tan(x)/x), x, 0, '-') == -2


def test_issue_14355():
    # This test checks the leading term and series for the floor and ceil
    # function when arg0 evaluates to S.NaN.
    assert floor((x**3 + x)/(x**2 - x)).as_leading_term(x, cdir = 1) == -2
    assert floor((x**3 + x)/(x**2 - x)).as_leading_term(x, cdir = -1) == -1
    assert floor((cos(x) - 1)/x).as_leading_term(x, cdir = 1) == -1
    assert floor((cos(x) - 1)/x).as_leading_term(x, cdir = -1) == 0
    assert floor(sin(x)/x).as_leading_term(x, cdir = 1) == 0
    assert floor(sin(x)/x).as_leading_term(x, cdir = -1) == 0
    assert floor(-tan(x)/x).as_leading_term(x, cdir = 1) == -2
    assert floor(-tan(x)/x).as_leading_term(x, cdir = -1) == -2
    assert floor(sin(x)/x/3).as_leading_term(x, cdir = 1) == 0
    assert floor(sin(x)/x/3).as_leading_term(x, cdir = -1) == 0
    assert ceiling((x**3 + x)/(x**2 - x)).as_leading_term(x, cdir = 1) == -1
    assert ceiling((x**3 + x)/(x**2 - x)).as_leading_term(x, cdir = -1) == 0
    assert ceiling((cos(x) - 1)/x).as_leading_term(x, cdir = 1) == 0
    assert ceiling((cos(x) - 1)/x).as_leading_term(x, cdir = -1) == 1
    assert ceiling(sin(x)/x).as_leading_term(x, cdir = 1) == 1
    assert ceiling(sin(x)/x).as_leading_term(x, cdir = -1) == 1
    assert ceiling(-tan(x)/x).as_leading_term(x, cdir = 1) == -1
    assert ceiling(-tan(x)/x).as_leading_term(x, cdir = 1) == -1
    assert ceiling(sin(x)/x/3).as_leading_term(x, cdir = 1) == 1
    assert ceiling(sin(x)/x/3).as_leading_term(x, cdir = -1) == 1
    # test for series
    assert floor(sin(x)/x).series(x, 0, 100, cdir = 1) == 0
    assert floor(sin(x)/x).series(x, 0, 100, cdir = 1) == 0
    assert floor((x**3 + x)/(x**2 - x)).series(x, 0, 100, cdir = 1) == -2
    assert floor((x**3 + x)/(x**2 - x)).series(x, 0, 100, cdir = -1) == -1
    assert ceiling(sin(x)/x).series(x, 0, 100, cdir = 1) == 1
    assert ceiling(sin(x)/x).series(x, 0, 100, cdir = -1) == 1
    assert ceiling((x**3 + x)/(x**2 - x)).series(x, 0, 100, cdir = 1) == -1
    assert ceiling((x**3 + x)/(x**2 - x)).series(x, 0, 100, cdir = -1) == 0

