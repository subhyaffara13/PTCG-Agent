
def test_type():
    assert m.check_type(1) == m.DerivedClass1
    with pytest.raises(RuntimeError) as execinfo:
        m.check_type(0)

    assert "pybind11::detail::get_type_info: unable to find type info" in str(
        execinfo.value
    )
    assert "Invalid" in str(execinfo.value)

