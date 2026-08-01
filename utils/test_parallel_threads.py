
def test_parallel_threads(num_parallel_threads):
    results = []
    rng = np.random.default_rng(1234)
    v0 = rng.random(50)

    def worker():
        x = diags_array([1.0, -2.0, 1.0], offsets=[-1, 0, 1], shape=(50, 50))
        w, v = eigs(x, k=3, v0=v0)
        results.append(w)

        w, v = eigsh(x, k=3, v0=v0)
        results.append(w)

    nthreads = 9 // num_parallel_threads + 1
    threads = [threading.Thread(target=worker) for _ in range(nthreads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    worker()

    for r in results:
        assert_allclose(r, results[-1])

