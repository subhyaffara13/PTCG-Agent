import functools

def test__workers_wrapper():
    arr = np.linspace(0, np.pi)
    req = np.sin(arr * 2.0)

    with Pool(2) as p:
        v = user_of_workers(arr, workers=p.map, b=2)
        assert_equal(v, req)

    v = user_of_workers(arr, workers=None, b=2)
    assert_equal(v, req)

    v = user_of_workers(arr, workers=2, b=2)
    assert_equal(v, req)

    # assess if decorator works with partial functions
    part_f = functools.partial(user_of_workers, b=2)
    assert_equal(part_f(arr), req)

    with Pool(2) as p:
        part_f = functools.partial(user_of_workers, b=2, workers=p.map)
        assert_equal(part_f(arr), req)

