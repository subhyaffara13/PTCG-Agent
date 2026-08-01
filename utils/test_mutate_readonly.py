
def test_mutate_readonly(arr):
    arr.flags.writeable = False
    for func, args in (
        (m.mutate_data, ()),
        (m.mutate_data_t, ()),
        (m.mutate_at_t, (0, 0)),
    ):
        with pytest.raises(ValueError) as excinfo:
            func(arr, *args)
        assert str(excinfo.value) == "array is not writeable"

