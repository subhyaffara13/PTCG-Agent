
def test_reference_sensitive_optional():
    assert m.double_or_zero_refsensitive(None) == 0
    assert m.double_or_zero_refsensitive(42) == 84
    pytest.raises(TypeError, m.double_or_zero_refsensitive, "foo")

    assert m.half_or_none_refsensitive(0) is None
    assert m.half_or_none_refsensitive(42) == 21
    pytest.raises(TypeError, m.half_or_none_refsensitive, "foo")

    assert m.test_nullopt_refsensitive() == 42
    assert m.test_nullopt_refsensitive(None) == 42
    assert m.test_nullopt_refsensitive(42) == 42
    assert m.test_nullopt_refsensitive(43) == 43

    assert m.test_no_assign_refsensitive() == 42
    assert m.test_no_assign_refsensitive(None) == 42
    assert m.test_no_assign_refsensitive(m.NoAssign(43)) == 43
    pytest.raises(TypeError, m.test_no_assign_refsensitive, 43)

    holder = m.OptionalRefSensitiveHolder()
    mvalue = holder.member
    assert mvalue.initialized
    assert holder.member_initialized()

    props = m.OptionalRefSensitiveProperties()
    assert int(props.access_by_ref) == 42
    assert int(props.access_by_copy) == 42

