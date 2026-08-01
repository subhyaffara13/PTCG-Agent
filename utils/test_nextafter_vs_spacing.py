
def test_nextafter_vs_spacing():
    # XXX: spacing does not handle long double yet
    for t in [np.float32, np.float64]:
        for _f in [1, 1e-5, 1000]:
            f = t(_f)
            f1 = t(_f + 1)
            assert_(np.nextafter(f, f1) - f == np.spacing(f))

