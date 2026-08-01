
def test_lra_satask():
    im = Symbol('im', imaginary=True)

    # test preprocessing of unequalities is working correctly
    assert lra_satask(Q.eq(x, 1), ~Q.ne(x, 0)) is False
    assert lra_satask(Q.eq(x, 0), ~Q.ne(x, 0)) is True
    assert lra_satask(~Q.ne(x, 0), Q.eq(x, 0)) is True
    assert lra_satask(~Q.eq(x, 0), Q.eq(x, 0)) is False
    assert lra_satask(Q.ne(x, 0), Q.eq(x, 0)) is False

    # basic tests
    assert lra_satask(Q.ne(x, x)) is False
    assert lra_satask(Q.eq(x, x)) is True
    assert lra_satask(Q.gt(x, 0), Q.gt(x, 1)) is True

    # check that True/False are handled
    assert lra_satask(Q.gt(x, 0), True) is None
    assert raises(ValueError, lambda: lra_satask(Q.gt(x, 0), False))

    # check imaginary numbers are correctly handled
    # (im * I).is_real returns True so this is an edge case
    raises(UnhandledInput, lambda: lra_satask(Q.gt(im * I, 0), Q.gt(im * I, 0)))

    # check matrix inputs
    X = MatrixSymbol("X", 2, 2)
    raises(UnhandledInput, lambda: lra_satask(Q.lt(X, 2) & Q.gt(X, 3)))

