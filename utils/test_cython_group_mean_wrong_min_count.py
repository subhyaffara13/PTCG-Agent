
def test_cython_group_mean_wrong_min_count():
    actual = np.zeros(shape=(1, 1), dtype="float64")
    counts = np.zeros(1, dtype="int64")
    data = np.zeros(1, dtype="float64")[:, None]
    labels = np.zeros(1, dtype=np.intp)

    with pytest.raises(AssertionError, match="min_count"):
        group_mean(actual, counts, data, labels, is_datetimelike=True, min_count=0)

