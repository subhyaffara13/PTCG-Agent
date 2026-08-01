
def test_iter_reduction_error():

    a = np.arange(6)
    assert_raises(ValueError, nditer, [a, None], [],
                    [['readonly'], ['readwrite', 'allocate']],
                    op_axes=[[0], [-1]])

    a = np.arange(6).reshape(2, 3)
    assert_raises(ValueError, nditer, [a, None], ['external_loop'],
                    [['readonly'], ['readwrite', 'allocate']],
                    op_axes=[[0, 1], [-1, -1]])

