
def test_dct2_definition_matlab(mdata_xy, rdt):
    # Test correspondence with matlab (orthornomal mode).
    dt = np.result_type(np.float32, rdt)
    x = np.array(mdata_xy[0], dtype=dt)

    yr = mdata_xy[1]
    y = dct(x, norm="ortho", type=2)
    dec = dec_map[(dct, rdt, 2)]
    assert_equal(y.dtype, dt)
    assert_array_almost_equal(y, yr, decimal=dec)

