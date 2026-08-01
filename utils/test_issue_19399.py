
def test_issue_19399():
    if not numpy:
        skip("numpy not installed.")

    a = numpy.array(Rational(1, 2))
    b = Rational(1, 3)
    assert (a * b, type(a * b)) == (b * a, type(b * a))

