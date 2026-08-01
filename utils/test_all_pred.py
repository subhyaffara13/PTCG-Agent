
def test_all_pred():
    # test usable pred
    assert lra_satask(Q.extended_positive(x), (x > 2)) is True
    assert lra_satask(Q.positive_infinite(x)) is False
    assert lra_satask(Q.negative_infinite(x)) is False

    # test disallowed pred
    raises(UnhandledInput, lambda: lra_satask((x > 0), (x > 2) & Q.prime(x)))
    raises(UnhandledInput, lambda: lra_satask((x > 0), (x > 2) & Q.composite(x)))
    raises(UnhandledInput, lambda: lra_satask((x > 0), (x > 2) & Q.odd(x)))
    raises(UnhandledInput, lambda: lra_satask((x > 0), (x > 2) & Q.even(x)))
    raises(UnhandledInput, lambda: lra_satask((x > 0), (x > 2) & Q.integer(x)))

