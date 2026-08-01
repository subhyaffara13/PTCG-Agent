
def test_stack():
    # non-iterable input
    assert_raises(TypeError, stack, 1)

    # 0d input
    for input_ in [(1, 2, 3),
                   [np.int32(1), np.int32(2), np.int32(3)],
                   [np.array(1), np.array(2), np.array(3)]]:
        assert_array_equal(stack(input_), [1, 2, 3])
    # 1d input examples
    a = np.array([1, 2, 3])
    b = np.array([4, 5, 6])
    r1 = array([[1, 2, 3], [4, 5, 6]])
    assert_array_equal(np.stack((a, b)), r1)
    assert_array_equal(np.stack((a, b), axis=1), r1.T)
    # all input types
    assert_array_equal(np.stack([a, b]), r1)
    assert_array_equal(np.stack(array([a, b])), r1)
    # all shapes for 1d input
    arrays = [np.random.randn(3) for _ in range(10)]
    axes = [0, 1, -1, -2]
    expected_shapes = [(10, 3), (3, 10), (3, 10), (10, 3)]
    for axis, expected_shape in zip(axes, expected_shapes):
        assert_equal(np.stack(arrays, axis).shape, expected_shape)
    assert_raises_regex(AxisError, 'out of bounds', stack, arrays, axis=2)
    assert_raises_regex(AxisError, 'out of bounds', stack, arrays, axis=-3)
    # all shapes for 2d input
    arrays = [np.random.randn(3, 4) for _ in range(10)]
    axes = [0, 1, 2, -1, -2, -3]
    expected_shapes = [(10, 3, 4), (3, 10, 4), (3, 4, 10),
                       (3, 4, 10), (3, 10, 4), (10, 3, 4)]
    for axis, expected_shape in zip(axes, expected_shapes):
        assert_equal(np.stack(arrays, axis).shape, expected_shape)
    # empty arrays
    assert_(stack([[], [], []]).shape == (3, 0))
    assert_(stack([[], [], []], axis=1).shape == (0, 3))
    # out
    out = np.zeros_like(r1)
    np.stack((a, b), out=out)
    assert_array_equal(out, r1)
    # edge cases
    assert_raises_regex(ValueError, 'need at least one array', stack, [])
    assert_raises_regex(ValueError, 'must have the same shape',
                        stack, [1, np.arange(3)])
    assert_raises_regex(ValueError, 'must have the same shape',
                        stack, [np.arange(3), 1])
    assert_raises_regex(ValueError, 'must have the same shape',
                        stack, [np.arange(3), 1], axis=1)
    assert_raises_regex(ValueError, 'must have the same shape',
                        stack, [np.zeros((3, 3)), np.zeros(3)], axis=1)
    assert_raises_regex(ValueError, 'must have the same shape',
                        stack, [np.arange(2), np.arange(3)])

    # do not accept generators
    with pytest.raises(TypeError, match="arrays to stack must be"):
        stack(x for x in range(3))

    # casting and dtype test
    a = np.array([1, 2, 3])
    b = np.array([2.5, 3.5, 4.5])
    res = np.stack((a, b), axis=1, casting="unsafe", dtype=np.int64)
    expected_res = np.array([[1, 2], [2, 3], [3, 4]])
    assert_array_equal(res, expected_res)
    # casting and dtype with TypeError
    with assert_raises(TypeError):
        stack((a, b), dtype=np.int64, axis=1, casting="safe")


def test_stack():
    # 2018-04-29: copied here from core.tests.test_shape_base
    # check np.matrix cannot be stacked
    m = np.matrix([[1, 2], [3, 4]])
    assert_raises_regex(ValueError, 'shape too large to be a matrix',
                        np.stack, [m, m])

