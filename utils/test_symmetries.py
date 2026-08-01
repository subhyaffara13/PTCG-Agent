
def test_symmetries():
    np.random.seed(1234)
    a, h = np.random.rand(100), np.random.rand(100)
    assert_equal(sc.owens_t(h, a), sc.owens_t(-h, a))
    assert_equal(sc.owens_t(h, a), -sc.owens_t(h, -a))

