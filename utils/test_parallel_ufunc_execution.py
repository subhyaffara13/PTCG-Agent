
def test_parallel_ufunc_execution():
    # if the loop data cache or dispatch cache are not thread-safe
    # computing ufuncs simultaneously in multiple threads leads
    # to a data race that causes crashes or spurious exceptions
    for dtype in [np.float32, np.float64, np.int32]:
        for op in [np.random.random((25,)).astype(dtype), dtype(25)]:
            for ufunc in [np.isnan, np.sin]:
                run_threaded(lambda: ufunc(op), 500)

    # see gh-26690
    NUM_THREADS = 50

    a = np.ones(1000)

    def f(b):
        b.wait()
        return a.sum()

    run_threaded(f, NUM_THREADS, pass_barrier=True)

