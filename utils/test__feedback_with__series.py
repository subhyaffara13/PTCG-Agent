
def test_Feedback_with_Series():
    # Solves issue https://github.com/sympy/sympy/issues/26161
    tf1 = TransferFunction(s+1, 1, s)
    tf2 = TransferFunction(s+2, 1, s)
    fd1 = Feedback(tf1, tf2, -1) # Negative Feedback system
    fd2 = Feedback(tf1, tf2, 1) # Positive Feedback system
    unit = TransferFunction(1, 1, s)

    # Checking the type
    assert isinstance(fd1, SISOLinearTimeInvariant)
    assert isinstance(fd1, Feedback)

    # Testing the numerator and denominator
    assert fd1.num == tf1
    assert fd2.num == tf1
    assert fd1.den == Parallel(unit, Series(tf2, tf1))
    assert fd2.den == Parallel(unit, -Series(tf2, tf1))

    # Testing the Series and Parallel Combination with Feedback and TransferFunction
    s1 = Series(tf1, fd1)
    p1 = Parallel(tf1, fd1)
    assert tf1 * fd1 == s1
    assert tf1 + fd1 == p1
    assert s1.doit() == TransferFunction((s + 1)**2, (s + 1)*(s + 2) + 1, s)
    assert p1.doit() == TransferFunction(s + (s + 1)*((s + 1)*(s + 2) + 1) + 1, (s + 1)*(s + 2) + 1, s)

    # Testing the use of Feedback and TransferFunction with Feedback
    fd3 = Feedback(tf1*fd1, tf2, -1)
    assert fd3 == Feedback(Series(tf1, fd1), tf2)
    assert fd3.num == tf1 * fd1
    assert fd3.den == Parallel(unit, Series(tf2, Series(tf1, fd1)))

    # Testing the use of Feedback and TransferFunction with TransferFunction
    tf3 = TransferFunction(tf1*fd1, tf2, s)
    assert tf3 == TransferFunction(Series(tf1, fd1), tf2, s)
    assert tf3.num == tf1*fd1

