
def test_idct_definition(fftwdata_size, rdt, type, reference_data, ref_lock):
    with ref_lock:
        xr, yr, dt = fftw_dct_ref(type, fftwdata_size, rdt, reference_data)
    x = idct(yr, type=type)
    dec = dec_map[(idct, rdt, type)]
    assert_equal(x.dtype, dt)
    assert_allclose(x, xr, rtol=0., atol=np.max(xr)*10**(-dec))

