
def test_mask_shape_assignment_does_not_break_masked():
    a = np.ma.masked
    b = np.ma.array(1, mask=a.mask)
    with pytest.warns(DeprecationWarning):  # gh-29492
        b.shape = (1,)
    assert_equal(a.mask.shape, ())

