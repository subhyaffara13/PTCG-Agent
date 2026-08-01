
def test_integer_comparison(sctype, other_val, comp):
    # Test that comparisons with integers (especially out-of-bound) ones
    # works correctly.
    val_obj = 10
    val = sctype(val_obj)
    # Check that the scalar behaves the same as the python int:
    assert comp(10, other_val) == comp(val, other_val)
    assert comp(val, other_val) == comp(10, other_val)
    # Except for the result type:
    assert type(comp(val, other_val)) is np.bool

    # Check that the integer array and object array behave the same:
    val_obj = np.array([10, 10], dtype=object)
    val = val_obj.astype(sctype)
    assert_array_equal(comp(val_obj, other_val), comp(val, other_val))
    assert_array_equal(comp(other_val, val_obj), comp(other_val, val))

