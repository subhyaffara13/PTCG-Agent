
def test_Add_as_content_primitive():
    assert (x + 2).as_content_primitive() == (1, x + 2)

    assert (3*x + 2).as_content_primitive() == (1, 3*x + 2)
    assert (3*x + 3).as_content_primitive() == (3, x + 1)
    assert (3*x + 6).as_content_primitive() == (3, x + 2)

    assert (3*x + 2*y).as_content_primitive() == (1, 3*x + 2*y)
    assert (3*x + 3*y).as_content_primitive() == (3, x + y)
    assert (3*x + 6*y).as_content_primitive() == (3, x + 2*y)

    assert (3/x + 2*x*y*z**2).as_content_primitive() == (1, 3/x + 2*x*y*z**2)
    assert (3/x + 3*x*y*z**2).as_content_primitive() == (3, 1/x + x*y*z**2)
    assert (3/x + 6*x*y*z**2).as_content_primitive() == (3, 1/x + 2*x*y*z**2)

    assert (2*x/3 + 4*y/9).as_content_primitive() == \
        (Rational(2, 9), 3*x + 2*y)
    assert (2*x/3 + 2.5*y).as_content_primitive() == \
        (Rational(1, 3), 2*x + 7.5*y)

    # the coefficient may sort to a position other than 0
    p = 3 + x + y
    assert (2*p).expand().as_content_primitive() == (2, p)
    assert (2.0*p).expand().as_content_primitive() == (1, 2.*p)
    p *= -1
    assert (2*p).expand().as_content_primitive() == (2, p)

