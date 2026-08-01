
def test_issue_14706():
    if not numpy:
        skip("numpy not installed.")

    z1 = numpy.zeros((1, 1), dtype=numpy.float64)
    z2 = numpy.zeros((2, 2), dtype=numpy.float64)
    z3 = numpy.zeros((), dtype=numpy.float64)

    y1 = numpy.ones((1, 1), dtype=numpy.float64)
    y2 = numpy.ones((2, 2), dtype=numpy.float64)
    y3 = numpy.ones((), dtype=numpy.float64)

    assert numpy.all(x + z1 == numpy.full((1, 1), x))
    assert numpy.all(x + z2 == numpy.full((2, 2), x))
    assert numpy.all(z1 + x == numpy.full((1, 1), x))
    assert numpy.all(z2 + x == numpy.full((2, 2), x))
    for z in [z3,
              numpy.int64(0),
              numpy.float64(0),
              numpy.complex64(0)]:
        assert x + z == x
        assert z + x == x
        assert isinstance(x + z, Symbol)
        assert isinstance(z + x, Symbol)

    # If these tests fail, then it means that numpy has finally
    # fixed the issue of scalar conversion for rank>0 arrays
    # which is mentioned in numpy/numpy#10404. In that case,
    # some changes have to be made in sympify.py.
    # Note: For future reference, for anyone who takes up this
    # issue when numpy has finally fixed their side of the problem,
    # the changes for this temporary fix were introduced in PR 18651
    assert numpy.all(x + y1 == numpy.full((1, 1), x + 1.0))
    assert numpy.all(x + y2 == numpy.full((2, 2), x + 1.0))
    assert numpy.all(y1 + x == numpy.full((1, 1), x + 1.0))
    assert numpy.all(y2 + x == numpy.full((2, 2), x + 1.0))
    for y_ in [y3,
              numpy.int64(1),
              numpy.float64(1),
              numpy.complex64(1)]:
        assert x + y_ == y_ + x
        assert isinstance(x + y_, Add)
        assert isinstance(y_ + x, Add)

    assert x + numpy.array(x) == 2 * x
    assert x + numpy.array([x]) == numpy.array([2*x], dtype=object)

    assert sympify(numpy.array([1])) == ImmutableDenseNDimArray([1], 1)
    assert sympify(numpy.array([[[1]]])) == ImmutableDenseNDimArray([1], (1, 1, 1))
    assert sympify(z1) == ImmutableDenseNDimArray([0.0], (1, 1))
    assert sympify(z2) == ImmutableDenseNDimArray([0.0, 0.0, 0.0, 0.0], (2, 2))
    assert sympify(z3) == ImmutableDenseNDimArray([0.0], ())
    assert sympify(z3, strict=True) == 0.0

    raises(SympifyError, lambda: sympify(numpy.array([1]), strict=True))
    raises(SympifyError, lambda: sympify(z1, strict=True))
    raises(SympifyError, lambda: sympify(z2, strict=True))

