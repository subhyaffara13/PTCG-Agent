
def test_rng_deepcopy_pickle():
    # test behavior of `rng` attribute and copy behavior
    kwargs = dict(a=[-1, 2], b=10)
    dist1 = Uniform(**kwargs)
    dist2 = deepcopy(dist1)
    dist3 = pickle.loads(pickle.dumps(dist1))

    res1, res2, res3 = dist1.sample(), dist2.sample(), dist3.sample()
    assert np.all(res2 != res1)
    assert np.all(res3 != res1)

    res1, res2, res3 = dist1.sample(rng=42), dist2.sample(rng=42), dist3.sample(rng=42)
    assert np.all(res2 == res1)
    assert np.all(res3 == res1)

