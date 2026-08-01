
def test_dijkstra_min_only_random(n):
    rng = np.random.default_rng(7345782358920239234)
    data = scipy.sparse.random_array((n, n), density=0.5, format='lil',
                                     rng=rng, dtype=np.float64)
    data.setdiag(np.zeros(n, dtype=np.bool_))
    # choose some random vertices
    v = np.arange(n)
    rng.shuffle(v)
    indices = v[:int(n*.1)]
    ds, pred, sources = dijkstra(data,
                                 directed=True,
                                 indices=indices,
                                 min_only=True,
                                 return_predecessors=True)
    for k in range(n):
        p = pred[k]
        s = sources[k]
        while p != -9999:
            assert sources[p] == s
            p = pred[p]

