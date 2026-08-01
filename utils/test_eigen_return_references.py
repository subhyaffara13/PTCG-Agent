
def test_eigen_return_references():
    """Tests various ways of returning references and non-referencing copies"""

    primary = np.ones((10, 10))
    a = m.ReturnTester()
    a_get1 = a.get()
    assert not a_get1.flags.owndata
    assert a_get1.flags.writeable
    assign_both(a_get1, primary, 3, 3, 5)
    a_get2 = a.get_ptr()
    assert not a_get2.flags.owndata
    assert a_get2.flags.writeable
    assign_both(a_get1, primary, 2, 3, 6)

    a_view1 = a.view()
    assert not a_view1.flags.owndata
    assert not a_view1.flags.writeable
    with pytest.raises(ValueError):
        a_view1[2, 3] = 4
    a_view2 = a.view_ptr()
    assert not a_view2.flags.owndata
    assert not a_view2.flags.writeable
    with pytest.raises(ValueError):
        a_view2[2, 3] = 4

    a_copy1 = a.copy_get()
    assert a_copy1.flags.owndata
    assert a_copy1.flags.writeable
    np.testing.assert_array_equal(a_copy1, primary)
    a_copy1[7, 7] = -44  # Shouldn't affect anything else
    c1want = array_copy_but_one(primary, 7, 7, -44)
    a_copy2 = a.copy_view()
    assert a_copy2.flags.owndata
    assert a_copy2.flags.writeable
    np.testing.assert_array_equal(a_copy2, primary)
    a_copy2[4, 4] = -22  # Shouldn't affect anything else
    c2want = array_copy_but_one(primary, 4, 4, -22)

    a_ref1 = a.ref()
    assert not a_ref1.flags.owndata
    assert a_ref1.flags.writeable
    assign_both(a_ref1, primary, 1, 1, 15)
    a_ref2 = a.ref_const()
    assert not a_ref2.flags.owndata
    assert not a_ref2.flags.writeable
    with pytest.raises(ValueError):
        a_ref2[5, 5] = 33
    a_ref3 = a.ref_safe()
    assert not a_ref3.flags.owndata
    assert a_ref3.flags.writeable
    assign_both(a_ref3, primary, 0, 7, 99)
    a_ref4 = a.ref_const_safe()
    assert not a_ref4.flags.owndata
    assert not a_ref4.flags.writeable
    with pytest.raises(ValueError):
        a_ref4[7, 0] = 987654321

    a_copy3 = a.copy_ref()
    assert a_copy3.flags.owndata
    assert a_copy3.flags.writeable
    np.testing.assert_array_equal(a_copy3, primary)
    a_copy3[8, 1] = 11
    c3want = array_copy_but_one(primary, 8, 1, 11)
    a_copy4 = a.copy_ref_const()
    assert a_copy4.flags.owndata
    assert a_copy4.flags.writeable
    np.testing.assert_array_equal(a_copy4, primary)
    a_copy4[8, 4] = 88
    c4want = array_copy_but_one(primary, 8, 4, 88)

    a_block1 = a.block(3, 3, 2, 2)
    assert not a_block1.flags.owndata
    assert a_block1.flags.writeable
    a_block1[0, 0] = 55
    primary[3, 3] = 55
    a_block2 = a.block_safe(2, 2, 3, 2)
    assert not a_block2.flags.owndata
    assert a_block2.flags.writeable
    a_block2[2, 1] = -123
    primary[4, 3] = -123
    a_block3 = a.block_const(6, 7, 4, 3)
    assert not a_block3.flags.owndata
    assert not a_block3.flags.writeable
    with pytest.raises(ValueError):
        a_block3[2, 2] = -44444

    a_copy5 = a.copy_block(2, 2, 2, 3)
    assert a_copy5.flags.owndata
    assert a_copy5.flags.writeable
    np.testing.assert_array_equal(a_copy5, primary[2:4, 2:5])
    a_copy5[1, 1] = 777
    c5want = array_copy_but_one(primary[2:4, 2:5], 1, 1, 777)

    a_corn1 = a.corners()
    assert not a_corn1.flags.owndata
    assert a_corn1.flags.writeable
    a_corn1 *= 50
    a_corn1[1, 1] = 999
    primary[0, 0] = 50
    primary[0, 9] = 50
    primary[9, 0] = 50
    primary[9, 9] = 999
    a_corn2 = a.corners_const()
    assert not a_corn2.flags.owndata
    assert not a_corn2.flags.writeable
    with pytest.raises(ValueError):
        a_corn2[1, 0] = 51

    # All of the changes made all the way along should be visible everywhere
    # now (except for the copies, of course)
    np.testing.assert_array_equal(a_get1, primary)
    np.testing.assert_array_equal(a_get2, primary)
    np.testing.assert_array_equal(a_view1, primary)
    np.testing.assert_array_equal(a_view2, primary)
    np.testing.assert_array_equal(a_ref1, primary)
    np.testing.assert_array_equal(a_ref2, primary)
    np.testing.assert_array_equal(a_ref3, primary)
    np.testing.assert_array_equal(a_ref4, primary)
    np.testing.assert_array_equal(a_block1, primary[3:5, 3:5])
    np.testing.assert_array_equal(a_block2, primary[2:5, 2:4])
    np.testing.assert_array_equal(a_block3, primary[6:10, 7:10])
    np.testing.assert_array_equal(
        a_corn1, primary[0 :: primary.shape[0] - 1, 0 :: primary.shape[1] - 1]
    )
    np.testing.assert_array_equal(
        a_corn2, primary[0 :: primary.shape[0] - 1, 0 :: primary.shape[1] - 1]
    )

    np.testing.assert_array_equal(a_copy1, c1want)
    np.testing.assert_array_equal(a_copy2, c2want)
    np.testing.assert_array_equal(a_copy3, c3want)
    np.testing.assert_array_equal(a_copy4, c4want)
    np.testing.assert_array_equal(a_copy5, c5want)

