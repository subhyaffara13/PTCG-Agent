
def test_collection_set_array():
    vals = [*range(10)]

    # Test set_array with list
    c = Collection()
    c.set_array(vals)

    # Test set_array with wrong dtype
    with pytest.raises(TypeError, match="^Image data of dtype"):
        c.set_array("wrong_input")

    # Test if array kwarg is copied
    vals[5] = 45
    assert np.not_equal(vals, c.get_array()).any()

