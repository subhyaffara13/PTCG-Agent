
def test_accessor_moves():
    inc_refs = m.accessor_moves()
    if inc_refs:
        assert inc_refs == [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
    else:
        pytest.skip("Not defined: PYBIND11_HANDLE_REF_DEBUG")

