
def test_log_leading_term():
    p = Symbol('p')

    # Test for STEP 3
    assert log(1 + x + x**2).as_leading_term(x, cdir=1) == x
    # Test for STEP 4
    assert log(2*x).as_leading_term(x, cdir=1) == log(x) + log(2)
    assert log(2*x).as_leading_term(x, cdir=-1) == log(x) + log(2)
    assert log(-2*x).as_leading_term(x, cdir=1, logx=p) == p + log(2) + I*pi
    assert log(-2*x).as_leading_term(x, cdir=-1, logx=p) == p + log(2) - I*pi
    # Test for STEP 5
    assert log(-2*x + (3 - I)*x**2).as_leading_term(x, cdir=1) == log(x) + log(2) - I*pi
    assert log(-2*x + (3 - I)*x**2).as_leading_term(x, cdir=-1) == log(x) + log(2) - I*pi
    assert log(2*x + (3 - I)*x**2).as_leading_term(x, cdir=1) == log(x) + log(2)
    assert log(2*x + (3 - I)*x**2).as_leading_term(x, cdir=-1) == log(x) + log(2) - 2*I*pi
    assert log(-1 + x - I*x**2 + I*x**3).as_leading_term(x, cdir=1) == -I*pi
    assert log(-1 + x - I*x**2 + I*x**3).as_leading_term(x, cdir=-1) == -I*pi
    assert log(-1/(1 - x)).as_leading_term(x, cdir=1) == I*pi
    assert log(-1/(1 - x)).as_leading_term(x, cdir=-1) == I*pi

