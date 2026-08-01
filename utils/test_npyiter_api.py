
def test_npyiter_api(install_temp):
    import checks
    arr = np.random.rand(3, 2)

    it = np.nditer(arr)
    assert checks.get_npyiter_size(it) == it.itersize == np.prod(arr.shape)
    assert checks.get_npyiter_ndim(it) == it.ndim == 1
    assert checks.npyiter_has_index(it) == it.has_index == False

    it = np.nditer(arr, flags=["c_index"])
    assert checks.npyiter_has_index(it) == it.has_index == True
    assert (
        checks.npyiter_has_delayed_bufalloc(it)
        == it.has_delayed_bufalloc
        == False
    )

    it = np.nditer(arr, flags=["buffered", "delay_bufalloc"])
    assert (
        checks.npyiter_has_delayed_bufalloc(it)
        == it.has_delayed_bufalloc
        == True
    )

    it = np.nditer(arr, flags=["multi_index"])
    assert checks.get_npyiter_size(it) == it.itersize == np.prod(arr.shape)
    assert checks.npyiter_has_multi_index(it) == it.has_multi_index == True
    assert checks.get_npyiter_ndim(it) == it.ndim == 2
    assert checks.test_get_multi_index_iter_next(it, arr)

    arr2 = np.random.rand(2, 1, 2)
    it = np.nditer([arr, arr2])
    assert checks.get_npyiter_nop(it) == it.nop == 2
    assert checks.get_npyiter_size(it) == it.itersize == 12
    assert checks.get_npyiter_ndim(it) == it.ndim == 3
    assert all(
        x is y for x, y in zip(checks.get_npyiter_operands(it), it.operands)
    )
    assert all(
        np.allclose(x, y)
        for x, y in zip(checks.get_npyiter_itviews(it), it.itviews)
    )

