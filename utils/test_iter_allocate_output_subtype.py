
def test_iter_allocate_output_subtype():
    # Make sure that the subtype with priority wins
    class MyNDArray(np.ndarray):
        __array_priority__ = 15

    # subclass vs ndarray
    a = np.array([[1, 2], [3, 4]]).view(MyNDArray)
    b = np.arange(4).reshape(2, 2).T
    i = nditer([a, b, None], [],
               [['readonly'], ['readonly'], ['writeonly', 'allocate']])
    assert_equal(type(a), type(i.operands[2]))
    assert_(type(b) is not type(i.operands[2]))
    assert_equal(i.operands[2].shape, (2, 2))

    # If subtypes are disabled, we should get back an ndarray.
    i = nditer([a, b, None], [],
               [['readonly'], ['readonly'],
                ['writeonly', 'allocate', 'no_subtype']])
    assert_equal(type(b), type(i.operands[2]))
    assert_(type(a) is not type(i.operands[2]))
    assert_equal(i.operands[2].shape, (2, 2))


def test_iter_allocate_output_subtype():
    # Make sure that the subtype with priority wins
    # 2018-04-29: moved here from core.tests.test_nditer, given the
    # matrix specific shape test.

    # matrix vs ndarray
    a = np.matrix([[1, 2], [3, 4]])
    b = np.arange(4).reshape(2, 2).T
    i = np.nditer([a, b, None], [],
                  [['readonly'], ['readonly'], ['writeonly', 'allocate']])
    assert_(type(i.operands[2]) is np.matrix)
    assert_(type(i.operands[2]) is not np.ndarray)
    assert_equal(i.operands[2].shape, (2, 2))

    # matrix always wants things to be 2D
    b = np.arange(4).reshape(1, 2, 2)
    assert_raises(RuntimeError, np.nditer, [a, b, None], [],
                  [['readonly'], ['readonly'], ['writeonly', 'allocate']])
    # but if subtypes are disabled, the result can still work
    i = np.nditer([a, b, None], [],
                  [['readonly'], ['readonly'],
                   ['writeonly', 'allocate', 'no_subtype']])
    assert_(type(i.operands[2]) is np.ndarray)
    assert_(type(i.operands[2]) is not np.matrix)
    assert_equal(i.operands[2].shape, (1, 2, 2))

