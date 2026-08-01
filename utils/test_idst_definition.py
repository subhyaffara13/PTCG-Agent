
def test_idst_definition(fftwdata_size, rdt, type, reference_data, ref_lock):
    with ref_lock:
        xr, yr, dt = fftw_dst_ref(type, fftwdata_size, rdt, reference_data)
    x = idst(yr, type=type)
    dec = dec_map[(idst, rdt, type)]
    assert_equal(x.dtype, dt)
    assert_allclose(x, xr, rtol=0., atol=np.max(xr)*10**(-dec))

