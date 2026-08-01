
def test_bxp_bad_capwidths():
    with pytest.raises(ValueError):
        _bxp_test_helper(bxp_kwargs=dict(capwidths=[1]))

