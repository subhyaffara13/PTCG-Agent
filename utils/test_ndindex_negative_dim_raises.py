
def test_ndindex_negative_dim_raises():
    # ndindex(-1) should raise a ValueError
    with pytest.raises(ValueError):
        list(np.ndindex(-1))

