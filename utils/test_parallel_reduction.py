
def test_parallel_reduction():
    # gh-28041
    NUM_THREADS = 50

    x = np.arange(1000)

    def closure(b):
        b.wait()
        np.sum(x)

    run_threaded(closure, NUM_THREADS, pass_barrier=True)

