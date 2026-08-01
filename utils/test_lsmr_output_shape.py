
def test_lsmr_output_shape():
    x = splin.lsmr(A=np.ones((10, 1)), b=np.zeros(10), x0=np.ones(1))[0]
    assert_equal(x.shape, (1,))

