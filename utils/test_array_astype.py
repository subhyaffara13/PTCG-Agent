
def test_array_astype():
    a = np.arange(6, dtype='f4').reshape(2, 3)
    # Default behavior: allows unsafe casts, keeps memory layout,
    #                   always copies.
    b = a.astype('i4')
    assert_equal(a, b)
    assert_equal(b.dtype, np.dtype('i4'))
    assert_equal(a.strides, b.strides)
    b = a.T.astype('i4')
    assert_equal(a.T, b)
    assert_equal(b.dtype, np.dtype('i4'))
    assert_equal(a.T.strides, b.strides)
    b = a.astype('f4')
    assert_equal(a, b)
    assert_(not (a is b))

    # copy=False parameter skips a copy
    b = a.astype('f4', copy=False)
    assert_(a is b)

    # order parameter allows overriding of the memory layout,
    # forcing a copy if the layout is wrong
    b = a.astype('f4', order='F', copy=False)
    assert_equal(a, b)
    assert_(not (a is b))
    assert_(b.flags.f_contiguous)

    b = a.astype('f4', order='C', copy=False)
    assert_equal(a, b)
    assert_(a is b)
    assert_(b.flags.c_contiguous)

    # casting parameter allows catching bad casts
    b = a.astype('c8', casting='safe')
    assert_equal(a, b)
    assert_equal(b.dtype, np.dtype('c8'))

    assert_raises(TypeError, a.astype, 'i4', casting='safe')

    # subok=False passes through a non-subclassed array
    b = a.astype('f4', subok=0, copy=False)
    assert_(a is b)

    class MyNDArray(np.ndarray):
        pass

    a = np.array([[0, 1, 2], [3, 4, 5]], dtype='f4').view(MyNDArray)

    # subok=True passes through a subclass
    b = a.astype('f4', subok=True, copy=False)
    assert_(a is b)

    # subok=True is default, and creates a subtype on a cast
    b = a.astype('i4', copy=False)
    assert_equal(a, b)
    assert_equal(type(b), MyNDArray)

    # subok=False never returns a subclass
    b = a.astype('f4', subok=False, copy=False)
    assert_equal(a, b)
    assert_(not (a is b))
    assert_(type(b) is not MyNDArray)

    # Make sure converting from string object to fixed length string
    # does not truncate.
    a = np.array([b'a' * 100], dtype='O')
    b = a.astype('S')
    assert_equal(a, b)
    assert_equal(b.dtype, np.dtype('S100'))
    a = np.array(['a' * 100], dtype='O')
    b = a.astype('U')
    assert_equal(a, b)
    assert_equal(b.dtype, np.dtype('U100'))

    # Same test as above but for strings shorter than 64 characters
    a = np.array([b'a' * 10], dtype='O')
    b = a.astype('S')
    assert_equal(a, b)
    assert_equal(b.dtype, np.dtype('S10'))
    a = np.array(['a' * 10], dtype='O')
    b = a.astype('U')
    assert_equal(a, b)
    assert_equal(b.dtype, np.dtype('U10'))

    a = np.array(123456789012345678901234567890, dtype='O').astype('S')
    assert_array_equal(a, np.array(b'1234567890' * 3, dtype='S30'))
    a = np.array(123456789012345678901234567890, dtype='O').astype('U')
    assert_array_equal(a, np.array('1234567890' * 3, dtype='U30'))

    a = np.array([123456789012345678901234567890], dtype='O').astype('S')
    assert_array_equal(a, np.array(b'1234567890' * 3, dtype='S30'))
    a = np.array([123456789012345678901234567890], dtype='O').astype('U')
    assert_array_equal(a, np.array('1234567890' * 3, dtype='U30'))

    a = np.array(123456789012345678901234567890, dtype='S')
    assert_array_equal(a, np.array(b'1234567890' * 3, dtype='S30'))
    a = np.array(123456789012345678901234567890, dtype='U')
    assert_array_equal(a, np.array('1234567890' * 3, dtype='U30'))

    a = np.array('a\u0140', dtype='U')
    b = np.ndarray(buffer=a, dtype='uint32', shape=2)
    assert_(b.size == 2)

    a = np.array([1000], dtype='i4')
    assert_raises(TypeError, a.astype, 'S1', casting='safe')

    a = np.array(1000, dtype='i4')
    assert_raises(TypeError, a.astype, 'U1', casting='safe')

    # gh-24023
    assert_raises(TypeError, a.astype)


def test_array_astype():
    # 2018-04-29: copied here from core.tests.test_api
    # subok=True passes through a matrix
    a = np.matrix([[0, 1, 2], [3, 4, 5]], dtype='f4')
    b = a.astype('f4', subok=True, copy=False)
    assert_(a is b)

    # subok=True is default, and creates a subtype on a cast
    b = a.astype('i4', copy=False)
    assert_equal(a, b)
    assert_equal(type(b), np.matrix)

    # subok=False never returns a matrix
    b = a.astype('f4', subok=False, copy=False)
    assert_equal(a, b)
    assert_(not (a is b))
    assert_(type(b) is not np.matrix)

