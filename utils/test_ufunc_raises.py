
def test_ufunc_raises():
    msg = "ufunc method 'at'"
    with pytest.raises(ValueError, match=msg):
        np.log.at(NA, 0)

