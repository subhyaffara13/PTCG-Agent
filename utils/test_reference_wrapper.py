
def test_reference_wrapper():
    """std::reference_wrapper for builtin and user types"""
    assert m.refwrap_builtin(42) == 420
    assert m.refwrap_usertype(UserType(42)) == 42
    assert m.refwrap_usertype_const(UserType(42)) == 42

    with pytest.raises(TypeError) as excinfo:
        m.refwrap_builtin(None)
    assert "incompatible function arguments" in str(excinfo.value)

    with pytest.raises(TypeError) as excinfo:
        m.refwrap_usertype(None)
    assert "incompatible function arguments" in str(excinfo.value)

    assert m.refwrap_lvalue().value == 1
    assert m.refwrap_lvalue_const().value == 1

    a1 = m.refwrap_list(copy=True)
    a2 = m.refwrap_list(copy=True)
    assert [x.value for x in a1] == [2, 3]
    assert [x.value for x in a2] == [2, 3]
    assert a1[0] is not a2[0]
    assert a1[1] is not a2[1]

    b1 = m.refwrap_list(copy=False)
    b2 = m.refwrap_list(copy=False)
    assert [x.value for x in b1] == [1, 2]
    assert [x.value for x in b2] == [1, 2]
    assert b1[0] is b2[0]
    assert b1[1] is b2[1]

    assert m.refwrap_iiw(IncType(5)) == 5
    assert m.refwrap_call_iiw(IncType(10), m.refwrap_iiw) == [10, 10, 10, 10]

