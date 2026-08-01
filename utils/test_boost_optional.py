
def test_boost_optional():
    assert m.double_or_zero_boost(None) == 0
    assert m.double_or_zero_boost(42) == 84
    pytest.raises(TypeError, m.double_or_zero_boost, "foo")

    assert m.half_or_none_boost(0) is None
    assert m.half_or_none_boost(42) == 21
    pytest.raises(TypeError, m.half_or_none_boost, "foo")

    assert m.test_nullopt_boost() == 42
    assert m.test_nullopt_boost(None) == 42
    assert m.test_nullopt_boost(42) == 42
    assert m.test_nullopt_boost(43) == 43

    assert m.test_no_assign_boost() == 42
    assert m.test_no_assign_boost(None) == 42
    assert m.test_no_assign_boost(m.NoAssign(43)) == 43
    pytest.raises(TypeError, m.test_no_assign_boost, 43)

    holder = m.OptionalBoostHolder()
    mvalue = holder.member
    assert mvalue.initialized
    assert holder.member_initialized()

    props = m.OptionalBoostProperties()
    assert int(props.access_by_ref) == 42
    assert int(props.access_by_copy) == 42

