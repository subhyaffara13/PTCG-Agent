
def test_optional():
    assert m.double_or_zero(None) == 0
    assert m.double_or_zero(42) == 84
    pytest.raises(TypeError, m.double_or_zero, "foo")

    assert m.half_or_none(0) is None
    assert m.half_or_none(42) == 21
    pytest.raises(TypeError, m.half_or_none, "foo")

    assert m.test_nullopt() == 42
    assert m.test_nullopt(None) == 42
    assert m.test_nullopt(42) == 42
    assert m.test_nullopt(43) == 43

    assert m.test_no_assign() == 42
    assert m.test_no_assign(None) == 42
    assert m.test_no_assign(m.NoAssign(43)) == 43
    pytest.raises(TypeError, m.test_no_assign, 43)

    assert m.nodefer_none_optional(None)

    holder = m.OptionalHolder()
    mvalue = holder.member
    assert mvalue.initialized
    assert holder.member_initialized()

    props = m.OptionalProperties()
    assert int(props.access_by_ref) == 42
    assert int(props.access_by_copy) == 42

