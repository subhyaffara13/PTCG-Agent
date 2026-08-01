
def test_issue_16772():
    # because there is a converter for tuple, the
    # args are only sympified without the flags being passed
    # along; list, on the other hand, is not converted
    # with a converter so its args are traversed later
    ans = [Rational(3, 10), Rational(1, 5)]
    assert sympify(('.3', '.2'), rational=True) == Tuple(*ans)

