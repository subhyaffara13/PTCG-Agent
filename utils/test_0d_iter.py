
def test_0d_iter():
    # Basic test for iteration of 0-d arrays:
    i = nditer([2, 3], ['multi_index'], [['readonly']] * 2)
    assert_equal(i.ndim, 0)
    assert_equal(next(i), (2, 3))
    assert_equal(i.multi_index, ())
    assert_equal(i.iterindex, 0)
    assert_raises(StopIteration, next, i)
    # test reset:
    i.reset()
    assert_equal(next(i), (2, 3))
    assert_raises(StopIteration, next, i)

    # test forcing to 0-d
    i = nditer(np.arange(5), ['multi_index'], [['readonly']], op_axes=[()])
    assert_equal(i.ndim, 0)
    assert_equal(len(i), 1)

    i = nditer(np.arange(5), ['multi_index'], [['readonly']],
               op_axes=[()], itershape=())
    assert_equal(i.ndim, 0)
    assert_equal(len(i), 1)

    # passing an itershape alone is not enough, the op_axes are also needed
    with assert_raises(ValueError):
        nditer(np.arange(5), ['multi_index'], [['readonly']], itershape=())

    # Test a more complex buffered casting case (same as another test above)
    sdt = [('a', 'f4'), ('b', 'i8'), ('c', 'c8', (2, 3)), ('d', 'O')]
    a = np.array(0.5, dtype='f4')
    i = nditer(a, ['buffered', 'refs_ok'], ['readonly'],
                    casting='unsafe', op_dtypes=sdt)
    vals = next(i)
    assert_equal(vals['a'], 0.5)
    assert_equal(vals['b'], 0)
    assert_equal(vals['c'], [[(0.5)] * 3] * 2)
    assert_equal(vals['d'], 0.5)

