
def test_multiprocess(func):
    # Test that fft still works after fork (gh-10422)

    with multiprocessing.Pool(2) as p:
        res = p.map(func, [np.ones(100) for _ in range(4)])

    expect = func(np.ones(100))
    for x in res:
        assert_allclose(x, expect)

