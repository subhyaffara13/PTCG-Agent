
def test_cython_group_mean_datetimelike():
    actual = np.zeros(shape=(1, 1), dtype="float64")
    counts = np.array([0], dtype="int64")
    data = (
        np.array(
            [
                np.timedelta64(2, "ns"),
                np.timedelta64(4, "ns"),
                np.timedelta64("NaT", "ns"),
            ],
            dtype="m8[ns]",
        )[:, None]
        .view("int64")
        .astype("float64")
    )
    labels = np.zeros(len(data), dtype=np.intp)

    group_mean(actual, counts, data, labels, is_datetimelike=True)

    tm.assert_numpy_array_equal(actual[:, 0], np.array([3], dtype="float64"))

