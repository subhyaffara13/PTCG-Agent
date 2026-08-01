
def test_arbitrary_number_of_ops():
    # 2*16 + 1 is still just a few kiB, so should be fast and easy to deal with
    # but larger than any small custom integer.
    ops = [np.arange(10) for a in range(2**16 + 1)]

    it = np.nditer(ops)
    for i, vals in enumerate(it):
        assert all(v == i for v in vals)

