
def test_multithreaded_sharing() -> None:
    from multiprocessing.pool import ThreadPool

    def fn():
        x, y, z = build_views("ab,bc,cd")

        with shared_intermediates():
            contract("ab,bc,cd->a", x, y, z)
            contract("ab,bc,cd->b", x, y, z)

            return len(get_sharing_cache())

    expected = fn()
    pool = ThreadPool(8)
    fs = [pool.apply_async(fn) for _ in range(16)]
    assert not currently_sharing()
    assert [f.get() for f in fs] == [expected] * 16
    pool.close()

