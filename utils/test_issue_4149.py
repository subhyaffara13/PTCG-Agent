
def test_issue_4149():
    assert floor(3 + pi*I + y*I) == 3 + floor(pi + y)*I
    assert floor(3*I + pi*I + y*I) == floor(3 + pi + y)*I
    assert floor(3 + E + pi*I + y*I) == 5 + floor(pi + y)*I


def test_issue_4149():
    assert (3 + I).is_complex
    assert (3 + I).is_imaginary is False
    assert (3*I + S.Pi*I).is_imaginary
    # as Zero.is_imaginary is False, see issue 7649
    y = Symbol('y', real=True)
    assert (3*I + S.Pi*I + y*I).is_imaginary is None
    p = Symbol('p', positive=True)
    assert (3*I + S.Pi*I + p*I).is_imaginary
    n = Symbol('n', negative=True)
    assert (-3*I - S.Pi*I + n*I).is_imaginary

    i = Symbol('i', imaginary=True)
    assert ([(i**a).is_imaginary for a in range(4)] ==
            [False, True, False, True])

    # tests from the PR #7887:
    e = S("-sqrt(3)*I/2 + 0.866025403784439*I")
    assert e.is_real is False
    assert e.is_imaginary

