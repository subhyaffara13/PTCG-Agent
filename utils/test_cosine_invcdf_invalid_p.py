
def test_cosine_invcdf_invalid_p():
    # Check that p values outside of [0, 1] return nan.
    assert np.isnan(_cosine_invcdf([-0.1, 1.1])).all()

