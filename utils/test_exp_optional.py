
def test_exp_optional():
    assert m.double_or_zero_exp(None) == 0
    assert m.double_or_zero_exp(42) == 84
    pytest.raises(TypeError, m.double_or_zero_exp, "foo")

    assert m.half_or_none_exp(0) is None
    assert m.half_or_none_exp(42) == 21
    pytest.raises(TypeError, m.half_or_none_exp, "foo")

    assert m.test_nullopt_exp() == 42
    assert m.test_nullopt_exp(None) == 42
    assert m.test_nullopt_exp(42) == 42
    assert m.test_nullopt_exp(43) == 43

    assert m.test_no_assign_exp() == 42
    assert m.test_no_assign_exp(None) == 42
    assert m.test_no_assign_exp(m.NoAssign(43)) == 43
    pytest.raises(TypeError, m.test_no_assign_exp, 43)

    holder = m.OptionalExpHolder()
    mvalue = holder.member
    assert mvalue.initialized
    assert holder.member_initialized()

    props = m.OptionalExpProperties()
    assert int(props.access_by_ref) == 42
    assert int(props.access_by_copy) == 42

