
def test_structured_threadsafety2():
    # Nonzero (and some other functions) should be threadsafe for
    # structured datatypes, see gh-15387. This test can behave randomly.
    from concurrent.futures import ThreadPoolExecutor

    # Create a deeply nested dtype to make a failure more likely:
    dt = np.dtype([("", "f8")])
    dt = np.dtype([("", dt)])
    dt = np.dtype([("", dt)] * 2)
    # The array should be large enough to likely run into threading issues
    arr = np.random.uniform(size=(5000, 4)).view(dt)[:, 0]

    def func(arr):
        arr.nonzero()

    tpe = ThreadPoolExecutor(max_workers=8)
    futures = [tpe.submit(func, arr) for _ in range(10)]
    for f in futures:
        f.result()

    assert arr.dtype is dt

