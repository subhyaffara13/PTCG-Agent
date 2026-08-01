
def test_iter_assign_mapping():
    a = np.arange(24, dtype='f8').reshape(2, 3, 4).T
    it = np.nditer(a, [], [['readwrite', 'updateifcopy']],
                       casting='same_kind', op_dtypes=[np.dtype('f4')])
    with it:
        it.operands[0][...] = 3
        it.operands[0][...] = 14
    assert_equal(a, 14)
    it = np.nditer(a, [], [['readwrite', 'updateifcopy']],
                       casting='same_kind', op_dtypes=[np.dtype('f4')])
    with it:
        x = it.operands[0][-1:1]
        x[...] = 14
        it.operands[0][...] = -1234
    assert_equal(a, -1234)
    # check for no warnings on dealloc
    x = None
    it = None

