
def test_no_nd_support_in_init(spcreator):
    with pytest.raises(ValueError, match="arrays don't.*support 3D"):
        spcreator(np.ones((3, 2, 4)))

