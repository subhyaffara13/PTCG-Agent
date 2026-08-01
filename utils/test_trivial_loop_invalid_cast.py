
def test_trivial_loop_invalid_cast():
    # This tests the fast-path "invalid cast", see gh-19904.
    with pytest.raises(TypeError,
            match="cast ufunc 'add' input 0"):
        # the void dtype definitely cannot cast to double:
        np.add(np.array(1, "i,i"), 3, signature="dd->d")

