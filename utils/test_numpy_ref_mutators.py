
def test_numpy_ref_mutators():
    """Tests numpy mutating Eigen matrices (for returned Eigen::Ref<...>s)"""

    m.reset_refs()  # In case another test already changed it

    zc = m.get_cm_ref()
    zcro = m.get_cm_const_ref()
    zr = m.get_rm_ref()
    zrro = m.get_rm_const_ref()

    assert [zc[1, 2], zcro[1, 2], zr[1, 2], zrro[1, 2]] == [23] * 4

    assert not zc.flags.owndata
    assert zc.flags.writeable
    assert not zr.flags.owndata
    assert zr.flags.writeable
    assert not zcro.flags.owndata
    assert not zcro.flags.writeable
    assert not zrro.flags.owndata
    assert not zrro.flags.writeable

    zc[1, 2] = 99
    expect = np.array([[11.0, 12, 13], [21, 22, 99], [31, 32, 33]])
    # We should have just changed zc, of course, but also zcro and the original eigen matrix
    assert np.all(zc == expect)
    assert np.all(zcro == expect)
    assert np.all(m.get_cm_ref() == expect)

    zr[1, 2] = 99
    assert np.all(zr == expect)
    assert np.all(zrro == expect)
    assert np.all(m.get_rm_ref() == expect)

    # Make sure the readonly ones are numpy-readonly:
    with pytest.raises(ValueError):
        zcro[1, 2] = 6
    with pytest.raises(ValueError):
        zrro[1, 2] = 6

    # We should be able to explicitly copy like this (and since we're copying,
    # the const should drop away)
    y1 = np.array(m.get_cm_const_ref())

    assert y1.flags.owndata
    assert y1.flags.writeable
    # We should get copies of the eigen data, which was modified above:
    assert y1[1, 2] == 99
    y1[1, 2] += 12
    assert y1[1, 2] == 111
    assert zc[1, 2] == 99  # Make sure we aren't referencing the original

