
def test_init_factory_signature(msg):
    with pytest.raises(TypeError) as excinfo:
        m.TestFactory1("invalid", "constructor", "arguments")
    assert (
        msg(excinfo.value)
        == """
        __init__(): incompatible constructor arguments. The following argument types are supported:
            1. m.factory_constructors.TestFactory1(arg0: m.factory_constructors.tag.unique_ptr_tag, arg1: int)
            2. m.factory_constructors.TestFactory1(arg0: str)
            3. m.factory_constructors.TestFactory1(arg0: m.factory_constructors.tag.pointer_tag)
            4. m.factory_constructors.TestFactory1(arg0: handle, arg1: int, arg2: handle)

        Invoked with: 'invalid', 'constructor', 'arguments'
    """
    )

    assert (
        msg(m.TestFactory1.__init__.__doc__)
        == """
        __init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: m.factory_constructors.TestFactory1, arg0: m.factory_constructors.tag.unique_ptr_tag, arg1: int) -> None

        2. __init__(self: m.factory_constructors.TestFactory1, arg0: str) -> None

        3. __init__(self: m.factory_constructors.TestFactory1, arg0: m.factory_constructors.tag.pointer_tag) -> None

        4. __init__(self: m.factory_constructors.TestFactory1, arg0: handle, arg1: int, arg2: handle) -> None
    """
    )

