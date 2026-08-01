
def test_iter_non_writable_attribute_deletion():
    it = np.nditer(np.ones(2))
    attr = ["value", "shape", "operands", "itviews", "has_delayed_bufalloc",
            "iterationneedsapi", "has_multi_index", "has_index", "dtypes",
            "ndim", "nop", "itersize", "finished"]

    for s in attr:
        assert_raises(AttributeError, delattr, it, s)

