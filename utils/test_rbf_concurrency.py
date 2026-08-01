
def test_rbf_concurrency():
    x = linspace(0, 10, 100)
    y0 = sin(x)
    y1 = cos(x)
    y = np.vstack([y0, y1]).T
    rbf = Rbf(x, y, mode='N-D')

    def worker_fn(_, interp, xp):
        interp(xp)

    _run_concurrent_barrier(10, worker_fn, rbf, x)

