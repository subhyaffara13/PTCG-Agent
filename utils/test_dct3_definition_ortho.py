
def test_dct3_definition_ortho(mdata_x, rdt):
    # Test orthornomal mode.
    x = np.array(mdata_x, dtype=rdt)
    dt = np.result_type(np.float32, rdt)
    y = dct(x, norm='ortho', type=2)
    xi = dct(y, norm="ortho", type=3)
    dec = dec_map[(dct, rdt, 3)]
    assert_equal(xi.dtype, dt)
    assert_array_almost_equal(xi, x, decimal=dec)

