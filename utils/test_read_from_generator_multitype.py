
def test_read_from_generator_multitype():
    def gen():
        for i in range(3):
            yield f"{i} {i / 4}"

    res = np.loadtxt(gen(), dtype="i, d", delimiter=" ")
    expected = np.array([(0, 0.0), (1, 0.25), (2, 0.5)], dtype="i, d")
    assert_equal(res, expected)

