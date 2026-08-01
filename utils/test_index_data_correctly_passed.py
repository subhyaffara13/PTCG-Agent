
def test_index_data_correctly_passed():
    # GH 43133
    pytest.importorskip("numba")

    def f(values, index):
        return np.mean(index)

    df = DataFrame({"group": ["A", "A", "B"], "v": [4, 5, 6]}, index=[-1, -2, -3])
    result = df.groupby("group").aggregate(f, engine="numba")
    expected = DataFrame(
        [-1.5, -3.0], columns=["v"], index=Index(["A", "B"], name="group")
    )
    tm.assert_frame_equal(result, expected)


def test_index_data_correctly_passed():
    # GH 43133
    pytest.importorskip("numba")

    def f(values, index):
        return index - 1

    df = DataFrame({"group": ["A", "A", "B"], "v": [4, 5, 6]}, index=[-1, -2, -3])
    result = df.groupby("group").transform(f, engine="numba")
    expected = DataFrame([-2.0, -3.0, -4.0], columns=["v"], index=[-1, -2, -3])
    tm.assert_frame_equal(result, expected)

