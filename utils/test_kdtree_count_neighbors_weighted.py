import itertools

def test_kdtree_count_neighbors_weighted(kdtree_class):
    rng = np.random.RandomState(1234)
    r = np.arange(0.05, 1, 0.05)

    A = rng.random(21).reshape((7,3))
    B = rng.random(45).reshape((15,3))

    wA = rng.random(7)
    wB = rng.random(15)

    kdA = kdtree_class(A)
    kdB = kdtree_class(B)

    nAB = kdA.count_neighbors(kdB, r, cumulative=False, weights=(wA,wB))

    # Compare against brute-force
    weights = wA[None, :] * wB[:, None]
    dist = np.linalg.norm(A[None, :, :] - B[:, None, :], axis=-1)
    expect = [np.sum(weights[(prev_radius < dist) & (dist <= radius)])
              for prev_radius, radius in zip(itertools.chain([0], r[:-1]), r)]
    assert_allclose(nAB, expect)

