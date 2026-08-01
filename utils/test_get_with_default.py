
def test_get_with_default():
    # GH#7725
    d0 = ["a", "b", "c", "d"]
    d1 = np.arange(4, dtype="int64")

    for data, index in ((d0, d1), (d1, d0)):
        s = Series(data, index=index)
        for i, d in zip(index, data):
            assert s.get(i) == d
            assert s.get(i, d) == d
            assert s.get(i, "z") == d

            assert s.get("e", "z") == "z"
            assert s.get("e", "e") == "e"

            assert s.get(10, "z") == "z"
            assert s.get(10, 10) == 10

