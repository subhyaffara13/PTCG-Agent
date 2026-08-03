import copy

def test_shared_ptr_and_references():
    s = m.SharedPtrRef()
    stats = ConstructorStats.get(m.A)
    assert stats.alive() == 2

    ref = s.ref  # init_holder_helper(holder_ptr=false, owned=false)
    assert stats.alive() == 2
    assert s.set_ref(ref)
    with pytest.raises(RuntimeError) as excinfo:
        assert s.set_holder(ref)
    assert "Unable to cast from non-held to held instance" in str(excinfo.value)

    copy = s.copy  # init_holder_helper(holder_ptr=false, owned=true)
    assert stats.alive() == 3
    assert s.set_ref(copy)
    assert s.set_holder(copy)

    holder_ref = s.holder_ref  # init_holder_helper(holder_ptr=true, owned=false)
    assert stats.alive() == 3
    assert s.set_ref(holder_ref)
    assert s.set_holder(holder_ref)

    holder_copy = s.holder_copy  # init_holder_helper(holder_ptr=true, owned=true)
    assert stats.alive() == 3
    assert s.set_ref(holder_copy)
    assert s.set_holder(holder_copy)

    del ref, copy, holder_ref, holder_copy, s
    assert stats.alive() == 0

