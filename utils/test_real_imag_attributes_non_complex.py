
def test_real_imag_attributes_non_complex(dtype):
    dtype = np.dtype(dtype)

    a = np.array([[1, 2, 3], [4, 5, 6]]).astype(dtype)
    assert a.real is a
    # One could imagine broadcasting, but doesn't right now:
    imag = a.imag
    assert imag.strides == a.strides
    assert imag.dtype == a.dtype
    # This part is rather unclear:
    assert (imag == np.zeros((), dtype=a.dtype)).all()
    assert imag.flags.writeable is False

    class myarr(np.ndarray):
        def __array_finalize__(self, obj):
            self.finalized_with = obj

    ma = a.view(myarr)
    assert ma.real is ma
    assert type(ma.imag) is myarr
    assert ma.imag.finalized_with is ma

