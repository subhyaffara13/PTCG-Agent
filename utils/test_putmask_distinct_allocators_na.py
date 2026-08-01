
def test_putmask_distinct_allocators_na(string_list):
    dt_a = get_dtype(None)
    dt_b = get_dtype(None)
    a = np.array(string_list, dtype=dt_a)
    b = np.array([None] + string_list[:0:-1], dtype=dt_b)
    assert a.dtype is not b.dtype
    mask = np.arange(len(string_list)) % 2 == 0
    np.putmask(a, mask, b)
    for i in range(len(string_list)):
        if i == 0:
            assert a[i] is None
        elif mask[i]:
            assert a[i] == string_list[-i]
        else:
            assert a[i] == string_list[i]

