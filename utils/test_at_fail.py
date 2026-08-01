
def test_at_fail(arr, dim):
    for func in m.at_t, m.mutate_at_t:
        with pytest.raises(IndexError) as excinfo:
            func(arr, *([0] * dim))
        assert str(excinfo.value) == f"index dimension mismatch: {dim} (ndim = 2)"

