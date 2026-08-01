
def test_override_ref():
    """#392/397: overriding reference-returning functions"""
    o = m.OverrideTest("asdf")

    # Not allowed (see associated .cpp comment)
    # i = o.str_ref()
    # assert o.str_ref() == "asdf"
    assert o.str_value() == "asdf"

    assert o.A_value().value == "hi"
    a = o.A_ref()
    assert a.value == "hi"
    a.value = "bye"
    assert a.value == "bye"

