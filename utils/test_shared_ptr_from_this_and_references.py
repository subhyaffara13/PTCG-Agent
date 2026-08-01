
def test_shared_ptr_from_this_and_references():
    s = m.SharedFromThisRef()
    stats = ConstructorStats.get(m.B)
    assert stats.alive() == 2

    ref = s.ref  # init_holder_helper(holder_ptr=false, owned=false, bad_wp=false)
    assert stats.alive() == 2
    assert s.set_ref(ref)
    assert s.set_holder(
        ref
    )  # std::enable_shared_from_this can create a holder from a reference

    bad_wp = s.bad_wp  # init_holder_helper(holder_ptr=false, owned=false, bad_wp=true)
    assert stats.alive() == 2
    assert s.set_ref(bad_wp)
    with pytest.raises(RuntimeError) as excinfo:
        assert s.set_holder(bad_wp)
    assert "Unable to cast from non-held to held instance" in str(excinfo.value)

    copy = s.copy  # init_holder_helper(holder_ptr=false, owned=true, bad_wp=false)
    assert stats.alive() == 3
    assert s.set_ref(copy)
    assert s.set_holder(copy)

    holder_ref = (
        s.holder_ref
    )  # init_holder_helper(holder_ptr=true, owned=false, bad_wp=false)
    assert stats.alive() == 3
    assert s.set_ref(holder_ref)
    assert s.set_holder(holder_ref)

    holder_copy = (
        s.holder_copy
    )  # init_holder_helper(holder_ptr=true, owned=true, bad_wp=false)
    assert stats.alive() == 3
    assert s.set_ref(holder_copy)
    assert s.set_holder(holder_copy)

    del ref, bad_wp, copy, holder_ref, holder_copy, s
    assert stats.alive() == 0

    z = m.SharedFromThisVirt.get()
    y = m.SharedFromThisVirt.get()
    assert y is z

