
def test_structured_advanced_indexing():
    # Test that copyswap(n) used by integer array indexing is threadsafe
    # for structured datatypes, see gh-15387. This test can behave randomly.

    # Create a deeply nested dtype to make a failure more likely:
    dt = np.dtype([("", "f8")])
    dt = np.dtype([("", dt)] * 2)
    dt = np.dtype([("", dt)] * 2)
    # The array should be large enough to likely run into threading issues
    arr = np.random.uniform(size=(6000, 8)).view(dt)[:, 0]

    rng = np.random.default_rng()

    def func(arr):
        indx = rng.integers(0, len(arr), size=6000, dtype=np.intp)
        arr[indx]

    tpe = concurrent.futures.ThreadPoolExecutor(max_workers=8)
    futures = [tpe.submit(func, arr) for _ in range(10)]
    for f in futures:
        f.result()

    assert arr.dtype is dt

