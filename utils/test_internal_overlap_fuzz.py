
def test_internal_overlap_fuzz():
    # Fuzz check; the brute-force check is fairly slow

    x = np.arange(1).astype(np.int8)

    overlap = 0
    no_overlap = 0
    min_count = 100

    rng = np.random.RandomState(1234)

    while min(overlap, no_overlap) < min_count:
        ndim = rng.randint(1, 4, dtype=np.intp)

        strides = tuple(rng.randint(-1000, 1000, dtype=np.intp)
                        for j in range(ndim))
        shape = tuple(rng.randint(1, 30, dtype=np.intp)
                      for j in range(ndim))

        a = as_strided(x, strides=strides, shape=shape)
        result = check_internal_overlap(a)

        if result:
            overlap += 1
        else:
            no_overlap += 1

