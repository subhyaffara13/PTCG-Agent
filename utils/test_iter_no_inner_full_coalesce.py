
def test_iter_no_inner_full_coalesce():
    # Check no_inner iterators which coalesce into a single inner loop

    for shape in [(5,), (3, 4), (2, 3, 4), (2, 3, 4, 3), (2, 3, 2, 2, 3)]:
        size = np.prod(shape)
        a = arange(size)
        # Test each combination of forward and backwards indexing
        for dirs in range(2**len(shape)):
            dirs_index = [slice(None)] * len(shape)
            for bit in range(len(shape)):
                if ((2**bit) & dirs):
                    dirs_index[bit] = slice(None, None, -1)
            dirs_index = tuple(dirs_index)

            aview = a.reshape(shape)[dirs_index]
            # C-order
            i = nditer(aview, ['external_loop'], [['readonly']])
            assert_equal(i.ndim, 1)
            assert_equal(i[0].shape, (size,))
            # Fortran-order
            i = nditer(aview.T, ['external_loop'], [['readonly']])
            assert_equal(i.ndim, 1)
            assert_equal(i[0].shape, (size,))
            # Other order
            if len(shape) > 2:
                i = nditer(aview.swapaxes(0, 1),
                                    ['external_loop'], [['readonly']])
                assert_equal(i.ndim, 1)
                assert_equal(i[0].shape, (size,))

