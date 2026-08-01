
def test_pow_pos_neg():
    assert satask(Q.nonnegative(x**2), Q.positive(x)) is True
    assert satask(Q.nonpositive(x**2), Q.positive(x)) is False
    assert satask(Q.positive(x**2), Q.positive(x)) is True
    assert satask(Q.negative(x**2), Q.positive(x)) is False
    assert satask(Q.real(x**2), Q.positive(x)) is True

    assert satask(Q.nonnegative(x**2), Q.negative(x)) is True
    assert satask(Q.nonpositive(x**2), Q.negative(x)) is False
    assert satask(Q.positive(x**2), Q.negative(x)) is True
    assert satask(Q.negative(x**2), Q.negative(x)) is False
    assert satask(Q.real(x**2), Q.negative(x)) is True

    assert satask(Q.nonnegative(x**2), Q.nonnegative(x)) is True
    assert satask(Q.nonpositive(x**2), Q.nonnegative(x)) is None
    assert satask(Q.positive(x**2), Q.nonnegative(x)) is None
    assert satask(Q.negative(x**2), Q.nonnegative(x)) is False
    assert satask(Q.real(x**2), Q.nonnegative(x)) is True

    assert satask(Q.nonnegative(x**2), Q.nonpositive(x)) is True
    assert satask(Q.nonpositive(x**2), Q.nonpositive(x)) is None
    assert satask(Q.positive(x**2), Q.nonpositive(x)) is None
    assert satask(Q.negative(x**2), Q.nonpositive(x)) is False
    assert satask(Q.real(x**2), Q.nonpositive(x)) is True

    assert satask(Q.nonnegative(x**3), Q.positive(x)) is True
    assert satask(Q.nonpositive(x**3), Q.positive(x)) is False
    assert satask(Q.positive(x**3), Q.positive(x)) is True
    assert satask(Q.negative(x**3), Q.positive(x)) is False
    assert satask(Q.real(x**3), Q.positive(x)) is True

    assert satask(Q.nonnegative(x**3), Q.negative(x)) is False
    assert satask(Q.nonpositive(x**3), Q.negative(x)) is True
    assert satask(Q.positive(x**3), Q.negative(x)) is False
    assert satask(Q.negative(x**3), Q.negative(x)) is True
    assert satask(Q.real(x**3), Q.negative(x)) is True

    assert satask(Q.nonnegative(x**3), Q.nonnegative(x)) is True
    assert satask(Q.nonpositive(x**3), Q.nonnegative(x)) is None
    assert satask(Q.positive(x**3), Q.nonnegative(x)) is None
    assert satask(Q.negative(x**3), Q.nonnegative(x)) is False
    assert satask(Q.real(x**3), Q.nonnegative(x)) is True

    assert satask(Q.nonnegative(x**3), Q.nonpositive(x)) is None
    assert satask(Q.nonpositive(x**3), Q.nonpositive(x)) is True
    assert satask(Q.positive(x**3), Q.nonpositive(x)) is False
    assert satask(Q.negative(x**3), Q.nonpositive(x)) is None
    assert satask(Q.real(x**3), Q.nonpositive(x)) is True

    # If x is zero, x**negative is not real.
    assert satask(Q.nonnegative(x**-2), Q.nonpositive(x)) is None
    assert satask(Q.nonpositive(x**-2), Q.nonpositive(x)) is None
    assert satask(Q.positive(x**-2), Q.nonpositive(x)) is None
    assert satask(Q.negative(x**-2), Q.nonpositive(x)) is None
    assert satask(Q.real(x**-2), Q.nonpositive(x)) is None

