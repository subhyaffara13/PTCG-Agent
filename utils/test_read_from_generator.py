
def test_read_from_generator():
    def gen():
        for i in range(4):
            yield f"{i},{2 * i},{i**2}"

    res = np.loadtxt(gen(), dtype=int, delimiter=",")
    expected = np.array([[0, 0, 0], [1, 2, 1], [2, 4, 4], [3, 6, 9]])
    assert_equal(res, expected)

