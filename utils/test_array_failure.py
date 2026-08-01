
def test_array_failure():
    with pytest.raises(ValueError) as excinfo:
        m.array_fail_test()
    assert str(excinfo.value) == "cannot create a pybind11::array from a nullptr"

    with pytest.raises(ValueError) as excinfo:
        m.array_t_fail_test()
    assert str(excinfo.value) == "cannot create a pybind11::array_t from a nullptr"

    with pytest.raises(ValueError) as excinfo:
        m.array_fail_test_negative_size()
    assert str(excinfo.value) == "negative dimensions are not allowed"

