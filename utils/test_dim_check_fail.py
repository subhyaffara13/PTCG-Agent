
def test_dim_check_fail(arr):
    for func in (
        m.index_at,
        m.index_at_t,
        m.offset_at,
        m.offset_at_t,
        m.data,
        m.data_t,
        m.mutate_data,
        m.mutate_data_t,
    ):
        with pytest.raises(IndexError) as excinfo:
            func(arr, 1, 2, 3)
        assert str(excinfo.value) == "too many indices for an array: 3 (ndim = 2)"

