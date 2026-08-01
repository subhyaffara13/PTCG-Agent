
def test_void_dtype__buffer__thread_safety():
    import inspect
    dt = np.dtype([('name', np.str_, 16), ('grades', np.float64, (2,))])
    x = np.array(('ndarray_scalar', (1.2, 3.0)), dtype=dt)[()]
    assert isinstance(x, np.void)
    flags = [inspect.BufferFlags.STRIDES, inspect.BufferFlags.READ]

    def func(b):
        b.wait()
        for i in range(100):
            x.__buffer__(flags[i % 2])

    run_threaded(func, max_workers=8, pass_barrier=True)

