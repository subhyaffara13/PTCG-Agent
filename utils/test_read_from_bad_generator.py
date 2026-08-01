
def test_read_from_bad_generator():
    def gen():
        yield from ["1,2", b"3, 5", 12738]

    with pytest.raises(
            TypeError, match=r"non-string returned while reading data"):
        np.loadtxt(gen(), dtype="i, i", delimiter=",")

