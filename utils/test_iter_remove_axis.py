
def test_iter_remove_axis():
    a = arange(24).reshape(2, 3, 4)

    i = nditer(a, ['multi_index'])
    i.remove_axis(1)
    assert_equal(list(i), a[:, 0, :].ravel())

    a = a[::-1, :, :]
    i = nditer(a, ['multi_index'])
    i.remove_axis(0)
    assert_equal(list(i), a[0, :, :].ravel())

