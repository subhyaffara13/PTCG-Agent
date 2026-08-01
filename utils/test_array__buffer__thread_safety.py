
def test_array__buffer__thread_safety():
    import inspect
    arr = np.arange(1000)
    flags = [inspect.BufferFlags.STRIDED, inspect.BufferFlags.READ]

    def func(b):
        b.wait()
        for i in range(100):
            arr.__buffer__(flags[i % 2])

    run_threaded(func, max_workers=8, pass_barrier=True)

