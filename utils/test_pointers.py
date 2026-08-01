
def test_pointers(msg):
    living_before = ConstructorStats.get(UserType).alive()
    assert m.get_void_ptr_value(m.return_void_ptr()) == 0x1234
    assert m.get_void_ptr_value(UserType())  # Should also work for other C++ types
    assert ConstructorStats.get(UserType).alive() == living_before

    with pytest.raises(TypeError) as excinfo:
        m.get_void_ptr_value([1, 2, 3])  # This should not work
    assert (
        msg(excinfo.value)
        == """
        get_void_ptr_value(): incompatible function arguments. The following argument types are supported:
            1. (arg0: capsule) -> int

        Invoked with: [1, 2, 3]
    """
    )

    assert m.return_null_str() is None
    assert m.get_null_str_value(m.return_null_str()) is not None

    ptr = m.return_unique_ptr()
    assert "StringList" in repr(ptr)
    assert m.print_opaque_list(ptr) == "Opaque list: [some value]"

