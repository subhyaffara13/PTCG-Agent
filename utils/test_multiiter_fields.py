
def test_multiiter_fields(install_temp, arrays):
    import checks
    bcast = np.broadcast(*arrays)

    assert bcast.ndim == checks.get_multiiter_number_of_dims(bcast)
    assert bcast.size == checks.get_multiiter_size(bcast)
    assert bcast.numiter == checks.get_multiiter_num_of_iterators(bcast)
    assert bcast.shape == checks.get_multiiter_shape(bcast)
    assert bcast.index == checks.get_multiiter_current_index(bcast)
    assert all(
        x.base is y.base
        for x, y in zip(bcast.iters, checks.get_multiiter_iters(bcast))
    )

