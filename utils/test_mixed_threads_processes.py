
def test_mixed_threads_processes(x):
    # Test that the fft threadpool is safe to use before & after fork

    expect = fft.fft(x, workers=2)

    with multiprocessing.Pool(2) as p:
        res = p.map(_mt_fft, [x for _ in range(4)])

    for r in res:
        assert_allclose(r, expect)

    fft.fft(x, workers=2)

