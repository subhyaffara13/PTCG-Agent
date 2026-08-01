
def test_array_no_inheritance():
    data_masked = np.ma.array([1, 2, 3], mask=[True, False, True])
    data_masked_units = ArrayNoInheritance(data_masked, 'meters')

    # Get the masked representation of the Quantity-like class
    new_array = np.ma.array(data_masked_units)
    assert_equal(data_masked.data, new_array.data)
    assert_equal(data_masked.mask, new_array.mask)
    # Test sharing the mask
    data_masked.mask = [True, False, False]
    assert_equal(data_masked.mask, new_array.mask)
    assert_(new_array.sharedmask)

    # Get the masked representation of the Quantity-like class
    new_array = np.ma.array(data_masked_units, copy=True)
    assert_equal(data_masked.data, new_array.data)
    assert_equal(data_masked.mask, new_array.mask)
    # Test that the mask is not shared when copy=True
    data_masked.mask = [True, False, True]
    assert_equal([True, False, False], new_array.mask)
    assert_(not new_array.sharedmask)

    # Get the masked representation of the Quantity-like class
    new_array = np.ma.array(data_masked_units, keep_mask=False)
    assert_equal(data_masked.data, new_array.data)
    # The change did not affect the original mask
    assert_equal(data_masked.mask, [True, False, True])
    # Test that the mask is False and not shared when keep_mask=False
    assert_(not new_array.mask)
    assert_(not new_array.sharedmask)

