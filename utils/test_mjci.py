
def test_mjci():
    # Tests the Marits-Jarrett estimator
    data = ma.array([77, 87, 88,114,151,210,219,246,253,262,
                     296,299,306,376,428,515,666,1310,2611])
    assert_almost_equal(ms.mjci(data),[55.76819,45.84028,198.87875],5)

