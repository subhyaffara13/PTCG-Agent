
def test_issue_8853():
    p = Symbol('x', even=True, positive=True)
    assert floor(-p - S.Half).is_even == False
    assert floor(-p + S.Half).is_even == True
    assert ceiling(p - S.Half).is_even == True
    assert ceiling(p + S.Half).is_even == False

    assert get_integer_part(S.Half, -1, {}, True) == (0, 0)
    assert get_integer_part(S.Half, 1, {}, True) == (1, 0)
    assert get_integer_part(Rational(-1, 2), -1, {}, True) == (-1, 0)
    assert get_integer_part(Rational(-1, 2), 1, {}, True) == (0, 0)

