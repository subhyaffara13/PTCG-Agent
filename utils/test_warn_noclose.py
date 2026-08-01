
def test_warn_noclose():
    a = np.arange(6, dtype='f4')
    au = a.byteswap()
    au = au.view(au.dtype.newbyteorder())
    with pytest.warns(RuntimeWarning):
        it = np.nditer(au, [], [['readwrite', 'updateifcopy']],
                       casting='equiv', op_dtypes=[np.dtype('f4')])
        del it

