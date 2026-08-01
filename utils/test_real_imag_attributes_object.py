
def test_real_imag_attributes_object():
    a = np.array([[1, 0.5 + 2j, 3, int], [4, 5j, "string", {}]], dtype=object)

    # NOTE(seberg): doing something for non-numbers is guesswork...
    real = np.array([[1, 0.5, 3, int.real], [4, 0, "string", {}]], dtype=object)
    imag = np.array([[0, 2, 0, int.imag], [0, 5, 0, 0]], dtype=object)

    assert_array_equal(a.real, real)
    assert_array_equal(a.imag, imag)
    assert a.real.dtype == object
    assert a.imag.dtype == object
    assert not np.may_share_memory(a.real, a)
    assert not np.may_share_memory(a.imag, a)
    assert not a.real.flags.writeable
    assert not a.imag.flags.writeable

    # Object returns new arrays via ufuncs, so call wrap
    class myarr(np.ndarray):
        def __array_wrap__(self, *args, **kwargs):
            ret = super().__array_wrap__(*args, **kwargs)
            ret.wrap_called = True
            return ret

    ma = a.view(myarr)
    assert ma.real.wrap_called
    assert ma.imag.wrap_called

