
def test_complementary_method_use():
    # Show that complementary methods are used as expected.
    # E.g., use 1 - CDF to compute SF if CDF is overridden but SF is not

    mp.dps = 50
    x = np.linspace(0, 1, 10)
    class MyDist(rd.ReferenceDistribution):
        def _cdf(self, x):
            return x

    dist = MyDist()
    assert_allclose(dist.sf(x), 1 - dist.cdf(x))

    class MyDist(rd.ReferenceDistribution):
        def _sf(self, x):
            return 1-x

    dist = MyDist()
    assert_allclose(dist.cdf(x), 1 - dist.sf(x))

    class MyDist(rd.ReferenceDistribution):
        def _ppf(self, x, guess):
            return x

    dist = MyDist()
    assert_allclose(dist.isf(x), dist.ppf(1-x))

    class MyDist(rd.ReferenceDistribution):
        def _isf(self, x, guess):
            return 1-x

    dist = MyDist()
    assert_allclose(dist.ppf(x), dist.isf(1-x))

