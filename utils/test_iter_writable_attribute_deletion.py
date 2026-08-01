
def test_iter_writable_attribute_deletion():
    it = np.nditer(np.ones(2))
    attr = ["multi_index", "index", "iterrange", "iterindex"]
    for s in attr:
        assert_raises(AttributeError, delattr, it, s)

