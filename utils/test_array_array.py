
def test_array_array():
    from sys import byteorder

    e = "<" if byteorder == "little" else ">"

    arr = m.create_array_array(3)
    assert str(arr.dtype).replace(" ", "") == (
        "{'names':['a','b','c','d'],"
        f"'formats':[('S4',(3,)),('{e}i4',(2,)),('u1',(3,)),('{e}f4',(4,2))],"
        "'offsets':[0,12,20,24],'itemsize':56}"
    )
    assert m.print_array_array(arr) == [
        "a={{A,B,C,D},{K,L,M,N},{U,V,W,X}},b={0,1},"
        "c={0,1,2},d={{0,1},{10,11},{20,21},{30,31}}",
        "a={{W,X,Y,Z},{G,H,I,J},{Q,R,S,T}},b={1000,1001},"
        "c={10,11,12},d={{100,101},{110,111},{120,121},{130,131}}",
        "a={{S,T,U,V},{C,D,E,F},{M,N,O,P}},b={2000,2001},"
        "c={20,21,22},d={{200,201},{210,211},{220,221},{230,231}}",
    ]
    assert arr["a"].tolist() == [
        [b"ABCD", b"KLMN", b"UVWX"],
        [b"WXYZ", b"GHIJ", b"QRST"],
        [b"STUV", b"CDEF", b"MNOP"],
    ]
    assert arr["b"].tolist() == [[0, 1], [1000, 1001], [2000, 2001]]
    assert m.create_array_array(0).dtype == arr.dtype


def test_array_array():
    tobj = type(object)
    ones11 = np.ones((1, 1), np.float64)
    tndarray = type(ones11)
    # Test is_ndarray
    assert_equal(np.array(ones11, dtype=np.float64), ones11)
    if HAS_REFCOUNT:
        old_refcount = sys.getrefcount(tndarray)
        np.array(ones11)
        assert_equal(old_refcount, sys.getrefcount(tndarray))

    # test None
    assert_equal(np.array(None, dtype=np.float64),
                 np.array(np.nan, dtype=np.float64))
    if HAS_REFCOUNT:
        old_refcount = sys.getrefcount(tobj)
        np.array(None, dtype=np.float64)
        assert_equal(old_refcount, sys.getrefcount(tobj))

    # test scalar
    assert_equal(np.array(1.0, dtype=np.float64),
                 np.ones((), dtype=np.float64))
    if HAS_REFCOUNT:
        old_refcount = sys.getrefcount(np.float64)
        np.array(np.array(1.0, dtype=np.float64), dtype=np.float64)
        assert_equal(old_refcount, sys.getrefcount(np.float64))

    # test string
    S2 = np.dtype((bytes, 2))
    S3 = np.dtype((bytes, 3))
    S5 = np.dtype((bytes, 5))
    assert_equal(np.array(b"1.0", dtype=np.float64),
                 np.ones((), dtype=np.float64))
    assert_equal(np.array(b"1.0").dtype, S3)
    assert_equal(np.array(b"1.0", dtype=bytes).dtype, S3)
    assert_equal(np.array(b"1.0", dtype=S2), np.array(b"1."))
    assert_equal(np.array(b"1", dtype=S5), np.ones((), dtype=S5))

    # test string
    U2 = np.dtype((str, 2))
    U3 = np.dtype((str, 3))
    U5 = np.dtype((str, 5))
    assert_equal(np.array("1.0", dtype=np.float64),
                 np.ones((), dtype=np.float64))
    assert_equal(np.array("1.0").dtype, U3)
    assert_equal(np.array("1.0", dtype=str).dtype, U3)
    assert_equal(np.array("1.0", dtype=U2), np.array("1."))
    assert_equal(np.array("1", dtype=U5), np.ones((), dtype=U5))

    builtins = getattr(__builtins__, '__dict__', __builtins__)
    assert_(hasattr(builtins, 'get'))

    # test memoryview
    dat = np.array(memoryview(b'1.0'), dtype=np.float64)
    assert_equal(dat, [49.0, 46.0, 48.0])
    assert_(dat.dtype.type is np.float64)

    dat = np.array(memoryview(b'1.0'))
    assert_equal(dat, [49, 46, 48])
    assert_(dat.dtype.type is np.uint8)

    # test array interface
    a = np.array(100.0, dtype=np.float64)
    o = type("o", (object,),
             {"__array_interface__": a.__array_interface__})
    assert_equal(np.array(o, dtype=np.float64), a)

    # test array_struct interface
    a = np.array([(1, 4.0, 'Hello'), (2, 6.0, 'World')],
                 dtype=[('f0', int), ('f1', float), ('f2', str)])
    o = type("o", (object,),
             {"__array_struct__": a.__array_struct__})
    # wasn't what I expected... is np.array(o) supposed to equal a ?
    # instead we get an array([...], dtype=">V18")
    assert_equal(bytes(np.array(o).data), bytes(a.data))

    # test __array__
    def custom__array__(self, dtype=None, copy=None):
        return np.array(100.0, dtype=dtype, copy=copy)

    o = type("o", (object,), {"__array__": custom__array__})()
    assert_equal(np.array(o, dtype=np.float64), np.array(100.0, np.float64))

    # test recursion
    nested = 1.5
    for i in range(ncu.MAXDIMS):
        nested = [nested]

    # no error
    np.array(nested)

    # Exceeds recursion limit
    assert_raises(ValueError, np.array, [nested], dtype=np.float64)

    # Try with lists...
    # float32
    assert_equal(np.array([None] * 10, dtype=np.float32),
                 np.full((10,), np.nan, dtype=np.float32))
    assert_equal(np.array([[None]] * 10, dtype=np.float32),
                 np.full((10, 1), np.nan, dtype=np.float32))
    assert_equal(np.array([[None] * 10], dtype=np.float32),
                 np.full((1, 10), np.nan, dtype=np.float32))
    assert_equal(np.array([[None] * 10] * 10, dtype=np.float32),
                 np.full((10, 10), np.nan, dtype=np.float32))
    # float64
    assert_equal(np.array([None] * 10, dtype=np.float64),
                 np.full((10,), np.nan, dtype=np.float64))
    assert_equal(np.array([[None]] * 10, dtype=np.float64),
                 np.full((10, 1), np.nan, dtype=np.float64))
    assert_equal(np.array([[None] * 10], dtype=np.float64),
                 np.full((1, 10), np.nan, dtype=np.float64))
    assert_equal(np.array([[None] * 10] * 10, dtype=np.float64),
                 np.full((10, 10), np.nan, dtype=np.float64))

    assert_equal(np.array([1.0] * 10, dtype=np.float64),
                 np.ones((10,), dtype=np.float64))
    assert_equal(np.array([[1.0]] * 10, dtype=np.float64),
                 np.ones((10, 1), dtype=np.float64))
    assert_equal(np.array([[1.0] * 10], dtype=np.float64),
                 np.ones((1, 10), dtype=np.float64))
    assert_equal(np.array([[1.0] * 10] * 10, dtype=np.float64),
                 np.ones((10, 10), dtype=np.float64))

    # Try with tuples
    assert_equal(np.array((None,) * 10, dtype=np.float64),
                 np.full((10,), np.nan, dtype=np.float64))
    assert_equal(np.array([(None,)] * 10, dtype=np.float64),
                 np.full((10, 1), np.nan, dtype=np.float64))
    assert_equal(np.array([(None,) * 10], dtype=np.float64),
                 np.full((1, 10), np.nan, dtype=np.float64))
    assert_equal(np.array([(None,) * 10] * 10, dtype=np.float64),
                 np.full((10, 10), np.nan, dtype=np.float64))

    assert_equal(np.array((1.0,) * 10, dtype=np.float64),
                 np.ones((10,), dtype=np.float64))
    assert_equal(np.array([(1.0,)] * 10, dtype=np.float64),
                 np.ones((10, 1), dtype=np.float64))
    assert_equal(np.array([(1.0,) * 10], dtype=np.float64),
                 np.ones((1, 10), dtype=np.float64))
    assert_equal(np.array([(1.0,) * 10] * 10, dtype=np.float64),
                 np.ones((10, 10), dtype=np.float64))

