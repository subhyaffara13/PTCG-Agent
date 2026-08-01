
def test_parallel_flat_iterator():
    # gh-28042
    x = np.arange(20).reshape(5, 4).T

    def closure(b):
        b.wait()
        for _ in range(100):
            list(x.flat)

    run_threaded(closure, outer_iterations=100, pass_barrier=True)

    # gh-28143
    def prepare_args():
        return [np.arange(10)]

    def closure(x, b):
        b.wait()
        for _ in range(100):
            y = np.arange(10)
            y.flat[x] = x

    run_threaded(closure, pass_barrier=True, prepare_args=prepare_args)

