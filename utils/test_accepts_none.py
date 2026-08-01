
def test_accepts_none(msg):
    a = m.NoneTester()
    assert m.no_none1(a) == 42
    assert m.no_none2(a) == 42
    assert m.no_none3(a) == 42
    assert m.no_none4(a) == 42
    assert m.no_none5(a) == 42
    assert m.ok_none1(a) == 42
    assert m.ok_none2(a) == 42
    assert m.ok_none3(a) == 42
    assert m.ok_none4(a) == 42
    assert m.ok_none5(a) == 42

    with pytest.raises(TypeError) as excinfo:
        m.no_none1(None)
    assert "incompatible function arguments" in str(excinfo.value)
    with pytest.raises(TypeError) as excinfo:
        m.no_none2(None)
    assert "incompatible function arguments" in str(excinfo.value)
    with pytest.raises(TypeError) as excinfo:
        m.no_none3(None)
    assert "incompatible function arguments" in str(excinfo.value)
    with pytest.raises(TypeError) as excinfo:
        m.no_none4(None)
    assert "incompatible function arguments" in str(excinfo.value)
    with pytest.raises(TypeError) as excinfo:
        m.no_none5(None)
    assert "incompatible function arguments" in str(excinfo.value)

    # The first one still raises because you can't pass None as a lvalue reference arg:
    with pytest.raises(TypeError) as excinfo:
        assert m.ok_none1(None) == -1
    assert (
        msg(excinfo.value)
        == """
        ok_none1(): incompatible function arguments. The following argument types are supported:
            1. (arg0: m.methods_and_attributes.NoneTester) -> int

        Invoked with: None
    """
    )

    # The rest take the argument as pointer or holder, and accept None:
    assert m.ok_none2(None) == -1
    assert m.ok_none3(None) == -1
    assert m.ok_none4(None) == -1
    assert m.ok_none5(None) == -1

    with pytest.raises(TypeError) as excinfo:
        m.no_none_kwarg(None)
    assert "incompatible function arguments" in str(excinfo.value)
    with pytest.raises(TypeError) as excinfo:
        m.no_none_kwarg(a=None)
    assert "incompatible function arguments" in str(excinfo.value)
    with pytest.raises(TypeError) as excinfo:
        m.no_none_kwarg_kw_only(None)
    assert "incompatible function arguments" in str(excinfo.value)
    with pytest.raises(TypeError) as excinfo:
        m.no_none_kwarg_kw_only(a=None)
    assert "incompatible function arguments" in str(excinfo.value)

