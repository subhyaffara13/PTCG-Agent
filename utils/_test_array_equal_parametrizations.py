
def _test_array_equal_parametrizations():
    """
    we pre-create arrays as we sometime want to pass the same instance
    and sometime not. Passing the same instances may not mean the array are
    equal, especially when containing None
    """
    # those are 0-d arrays, it used to be a special case
    # where (e0 == e0).all() would raise
    e0 = np.array(0, dtype="int")
    e1 = np.array(1, dtype="float")
    # x,y, nan_equal, expected_result
    yield (e0, e0.copy(), None, True)
    yield (e0, e0.copy(), False, True)
    yield (e0, e0.copy(), True, True)

    #
    yield (e1, e1.copy(), None, True)
    yield (e1, e1.copy(), False, True)
    yield (e1, e1.copy(), True, True)

    # Non-nanable - those cannot hold nans
    a12 = np.array([1, 2])
    a12b = a12.copy()
    a123 = np.array([1, 2, 3])
    a13 = np.array([1, 3])
    a34 = np.array([3, 4])

    aS1 = np.array(["a"], dtype="S1")
    aS1b = aS1.copy()
    aS1u4 = np.array([("a", 1)], dtype="S1,u4")
    aS1u4b = aS1u4.copy()

    yield (a12, a12b, None, True)
    yield (a12, a12, None, True)
    yield (a12, a123, None, False)
    yield (a12, a34, None, False)
    yield (a12, a13, None, False)
    yield (aS1, aS1b, None, True)
    yield (aS1, aS1, None, True)

    # Non-float dtype - equal_nan should have no effect,
    yield (a123, a123, None, True)
    yield (a123, a123, False, True)
    yield (a123, a123, True, True)
    yield (a123, a123.copy(), None, True)
    yield (a123, a123.copy(), False, True)
    yield (a123, a123.copy(), True, True)
    yield (a123.astype("float"), a123.astype("float"), None, True)
    yield (a123.astype("float"), a123.astype("float"), False, True)
    yield (a123.astype("float"), a123.astype("float"), True, True)

    # these can hold None
    b1 = np.array([1, 2, np.nan])
    b2 = np.array([1, np.nan, 2])
    b3 = np.array([1, 2, np.inf])
    b4 = np.array(np.nan)

    # instances are the same
    yield (b1, b1, None, False)
    yield (b1, b1, False, False)
    yield (b1, b1, True, True)

    # equal but not same instance
    yield (b1, b1.copy(), None, False)
    yield (b1, b1.copy(), False, False)
    yield (b1, b1.copy(), True, True)

    # same once stripped of Nan
    yield (b1, b2, None, False)
    yield (b1, b2, False, False)
    yield (b1, b2, True, False)

    # nan's not conflated with inf's
    yield (b1, b3, None, False)
    yield (b1, b3, False, False)
    yield (b1, b3, True, False)

    # all Nan
    yield (b4, b4, None, False)
    yield (b4, b4, False, False)
    yield (b4, b4, True, True)
    yield (b4, b4.copy(), None, False)
    yield (b4, b4.copy(), False, False)
    yield (b4, b4.copy(), True, True)

    t1 = b1.astype("timedelta64[D]")
    t2 = b2.astype("timedelta64[D]")

    # Timedeltas are particular
    yield (t1, t1, None, False)
    yield (t1, t1, False, False)
    yield (t1, t1, True, True)

    yield (t1, t1.copy(), None, False)
    yield (t1, t1.copy(), False, False)
    yield (t1, t1.copy(), True, True)

    yield (t1, t2, None, False)
    yield (t1, t2, False, False)
    yield (t1, t2, True, False)

    # Multi-dimensional array
    md1 = np.array([[0, 1], [np.nan, 1]])

    yield (md1, md1, None, False)
    yield (md1, md1, False, False)
    yield (md1, md1, True, True)
    yield (md1, md1.copy(), None, False)
    yield (md1, md1.copy(), False, False)
    yield (md1, md1.copy(), True, True)
    # both complexes are nan+nan.j but the same instance
    cplx1, cplx2 = [np.array([np.nan + np.nan * 1j])] * 2

    # only real or img are nan.
    cplx3, cplx4 = np.complex64(1, np.nan), np.complex64(np.nan, 1)

    # Complex values
    yield (cplx1, cplx2, None, False)
    yield (cplx1, cplx2, False, False)
    yield (cplx1, cplx2, True, True)

    # Complex values, 1+nan, nan+1j
    yield (cplx3, cplx4, None, False)
    yield (cplx3, cplx4, False, False)
    yield (cplx3, cplx4, True, True)

