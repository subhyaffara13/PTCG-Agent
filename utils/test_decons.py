
def test_decons(codes_list, shape):
    group_index = get_group_index(codes_list, shape, sort=True, xnull=True)
    codes_list2 = _decons_group_index(group_index, shape)

    for a, b in zip(codes_list, codes_list2, strict=True):
        tm.assert_numpy_array_equal(a, b)

