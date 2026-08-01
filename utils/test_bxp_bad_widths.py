
def test_bxp_bad_widths():
    with pytest.raises(ValueError):
        _bxp_test_helper(bxp_kwargs=dict(widths=[1]))

