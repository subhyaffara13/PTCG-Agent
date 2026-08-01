
def test_astype_basic(dt1, dt2):
    # See gh-12070
    src = np.ma.array(ones(3, dt1), fill_value=1)
    dst = src.astype(dt2)

    assert_(src.fill_value == 1)
    assert_(src.dtype == dt1)
    assert_(src.fill_value.dtype == dt1)

    assert_(dst.fill_value == 1)
    assert_(dst.dtype == dt2)
    assert_(dst.fill_value.dtype == dt2)

    assert_equal(src, dst)

