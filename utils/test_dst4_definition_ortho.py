
def test_dst4_definition_ortho(rdt, mdata_x):
    # Test orthornomal mode.
    dec = dec_map[(dst, rdt, 4)]
    x = np.array(mdata_x, dtype=rdt)
    dt = np.result_type(np.float32, rdt)
    y = dst(x, norm='ortho', type=4)
    y2 = naive_dst4(x, norm='ortho')
    assert_equal(y.dtype, dt)
    assert_array_almost_equal(y, y2, decimal=dec)

