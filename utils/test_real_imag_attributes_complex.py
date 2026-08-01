
def test_real_imag_attributes_complex(dtype, real_dt, variation):
    a = np.array([[1, 2j, 3], [4, 5j, 6]]).astype(dtype)
    real = np.array([[1, 0, 3], [4, 0, 6]], dtype=real_dt)
    imag = np.array([[0, 2, 0], [0, 5, 0]], dtype=real_dt)

    if variation == "transpose":
        a = a.T
        real = real.T
        imag = imag.T
    elif variation == "set_writeable":
        a.flags.writeable = False

    assert_array_equal(a.real, real)
    assert_array_equal(a.imag, imag)
    assert a.real.dtype == real_dt
    assert a.imag.dtype == real_dt
    assert np.may_share_memory(a.real, a)
    assert np.may_share_memory(a.imag, a)
    assert a.real.flags.writeable == a.flags.writeable
    assert a.imag.flags.writeable == a.flags.writeable

    class myarr(np.ndarray):
        def __array_finalize__(self, obj):
            self.finalized_with = obj

    ma = a.view(myarr)
    assert ma.real.finalized_with is ma
    assert ma.imag.finalized_with is ma

