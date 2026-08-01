
def test_noconvert_args(msg):
    a = m.ArgInspector()
    assert (
        msg(a.f("hi"))
        == """
        loading ArgInspector1 argument WITH conversion allowed.  Argument value = hi
    """
    )
    assert (
        msg(a.g("this is a", "this is b"))
        == """
        loading ArgInspector1 argument WITHOUT conversion allowed.  Argument value = this is a
        loading ArgInspector1 argument WITH conversion allowed.  Argument value = this is b
        13
        loading ArgInspector2 argument WITH conversion allowed.  Argument value = (default arg inspector 2)
    """
    )
    assert (
        msg(a.g("this is a", "this is b", 42))
        == """
        loading ArgInspector1 argument WITHOUT conversion allowed.  Argument value = this is a
        loading ArgInspector1 argument WITH conversion allowed.  Argument value = this is b
        42
        loading ArgInspector2 argument WITH conversion allowed.  Argument value = (default arg inspector 2)
    """
    )
    assert (
        msg(a.g("this is a", "this is b", 42, "this is d"))
        == """
        loading ArgInspector1 argument WITHOUT conversion allowed.  Argument value = this is a
        loading ArgInspector1 argument WITH conversion allowed.  Argument value = this is b
        42
        loading ArgInspector2 argument WITH conversion allowed.  Argument value = this is d
    """
    )
    assert (
        a.h("arg 1")
        == "loading ArgInspector2 argument WITHOUT conversion allowed.  Argument value = arg 1"
    )
    assert (
        msg(m.arg_inspect_func("A1", "A2"))
        == """
        loading ArgInspector2 argument WITH conversion allowed.  Argument value = A1
        loading ArgInspector1 argument WITHOUT conversion allowed.  Argument value = A2
    """
    )

    assert m.floats_preferred(4) == 2.0
    assert m.floats_only(4.0) == 2.0
    with pytest.raises(TypeError) as excinfo:
        m.floats_only(4)
    assert (
        msg(excinfo.value)
        == """
        floats_only(): incompatible function arguments. The following argument types are supported:
            1. (f: float) -> float

        Invoked with: 4
    """
    )

    assert m.ints_preferred(4) == 2
    assert m.ints_preferred(True) == 0
    with pytest.raises(TypeError) as excinfo:
        m.ints_preferred(4.0)
    assert (
        msg(excinfo.value)
        == """
        ints_preferred(): incompatible function arguments. The following argument types are supported:
            1. (i: int) -> int

        Invoked with: 4.0
    """
    )

    assert m.ints_only(4) == 2
    with pytest.raises(TypeError) as excinfo:
        m.ints_only(4.0)
    assert (
        msg(excinfo.value)
        == """
        ints_only(): incompatible function arguments. The following argument types are supported:
            1. (i: int) -> int

        Invoked with: 4.0
    """
    )

