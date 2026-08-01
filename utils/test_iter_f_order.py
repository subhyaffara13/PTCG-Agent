
def test_iter_f_order():
    # Test forcing F order

    # Test the ordering for 1-D to 5-D shapes
    for shape in [(5,), (3, 4), (2, 3, 4), (2, 3, 4, 3), (2, 3, 2, 2, 3)]:
        a = arange(np.prod(shape))
        # Test each combination of positive and negative strides
        for dirs in range(2**len(shape)):
            dirs_index = [slice(None)] * len(shape)
            for bit in range(len(shape)):
                if ((2**bit) & dirs):
                    dirs_index[bit] = slice(None, None, -1)
            dirs_index = tuple(dirs_index)

            aview = a.reshape(shape)[dirs_index]
            # C-order
            i = nditer(aview, order='F')
            assert_equal(list(i), aview.ravel(order='F'))
            # Fortran-order
            i = nditer(aview.T, order='F')
            assert_equal(list(i), aview.T.ravel(order='F'))
            # Other order
            if len(shape) > 2:
                i = nditer(aview.swapaxes(0, 1), order='F')
                assert_equal(list(i),
                                    aview.swapaxes(0, 1).ravel(order='F'))

