
def test_custom(msg):
    # Can we catch a MyException?
    with pytest.raises(m.MyException) as excinfo:
        m.throws1()
    assert msg(excinfo.value) == "this error should go to a custom type"

    # Can we translate to standard Python exceptions?
    with pytest.raises(RuntimeError) as excinfo:
        m.throws2()
    assert msg(excinfo.value) == "this error should go to a standard Python exception"

    # Can we handle unknown exceptions?
    with pytest.raises(RuntimeError) as excinfo:
        m.throws3()
    assert msg(excinfo.value) == "Caught an unknown exception!"

    # Can we delegate to another handler by rethrowing?
    with pytest.raises(m.MyException) as excinfo:
        m.throws4()
    assert msg(excinfo.value) == "this error is rethrown"

    # Can we fall-through to the default handler?
    with pytest.raises(RuntimeError) as excinfo:
        m.throws_logic_error()
    assert (
        msg(excinfo.value) == "this error should fall through to the standard handler"
    )

    # OverFlow error translation.
    with pytest.raises(OverflowError) as excinfo:
        m.throws_overflow_error()

    # Can we handle a helper-declared exception?
    with pytest.raises(m.MyException5) as excinfo:
        m.throws5()
    assert msg(excinfo.value) == "this is a helper-defined translated exception"

    # Exception subclassing:
    with pytest.raises(m.MyException5) as excinfo:
        m.throws5_1()
    assert msg(excinfo.value) == "MyException5 subclass"
    assert isinstance(excinfo.value, m.MyException5_1)

    with pytest.raises(m.MyException5_1) as excinfo:
        m.throws5_1()
    assert msg(excinfo.value) == "MyException5 subclass"

    with pytest.raises(m.MyException5) as excinfo:  # noqa: PT012
        try:
            m.throws5()
        except m.MyException5_1 as err:
            raise RuntimeError("Exception error: caught child from parent") from err
    assert msg(excinfo.value) == "this is a helper-defined translated exception"

