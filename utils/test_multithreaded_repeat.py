
def test_multithreaded_repeat():
    x0 = np.arange(10)

    def closure(b):
        b.wait()
        for _ in range(100):
            x = np.repeat(x0, 2, axis=0)[::2]

    run_threaded(closure, max_workers=10, pass_barrier=True)

