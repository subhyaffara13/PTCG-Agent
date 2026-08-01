
def test_background_gradient_gmap_array_raises(gmap, axis):
    # test when gmap as converted ndarray is bad shape
    df = DataFrame([[0, 0, 0], [0, 0, 0]])
    msg = "supplied 'gmap' is not correct shape"
    with pytest.raises(ValueError, match=msg):
        df.style.background_gradient(gmap=gmap, axis=axis)._compute()

