
def test_dct4_definition_ortho(mdata_x, rdt):
    # Test orthornomal mode.
    x = np.array(mdata_x, dtype=rdt)
    dt = np.result_type(np.float32, rdt)
    y = dct(x, norm='ortho', type=4)
    y2 = naive_dct4(x, norm='ortho')
    dec = dec_map[(dct, rdt, 4)]
    assert_equal(y.dtype, dt)
    assert_allclose(y, y2, rtol=0., atol=np.max(y2)*10**(-dec))

