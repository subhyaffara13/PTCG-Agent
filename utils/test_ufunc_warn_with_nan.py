
def test_ufunc_warn_with_nan(ufunc):
    # issue gh-15127
    # test that calling certain ufuncs with a non-standard `nan` value does not
    # emit a warning
    # `b` holds a 64 bit signaling nan: the most significant bit of the
    # significand is zero.
    b = np.array([0x7ff0000000000001], 'i8').view('f8')
    assert np.isnan(b)
    if ufunc.nin == 1:
        ufunc(b)
    elif ufunc.nin == 2:
        ufunc(b, b.copy())
    else:
        raise ValueError('ufunc with more than 2 inputs')

