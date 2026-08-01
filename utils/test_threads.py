
def test_threads():
    # Smoke test for parallel threaded execution; doesn't actually
    # check that code runs in parallel, but just that it produces
    # expected results.
    nthreads = 10
    niter = 100

    n = 20
    a = csr_matrix(np.ones([n, n]))
    bres = []

    class Worker(threading.Thread):
        def run(self):
            b = a.copy()
            for j in range(niter):
                _sparsetools.csr_plus_csr(n, n,
                                          a.indptr, a.indices, a.data,
                                          a.indptr, a.indices, a.data,
                                          b.indptr, b.indices, b.data)
            bres.append(b)

    threads = [Worker() for _ in range(nthreads)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    for b in bres:
        assert_(np.all(b.toarray() == 2))

