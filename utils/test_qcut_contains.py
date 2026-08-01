
def test_qcut_contains(scale, q, precision):
    # GH-59355
    arr = (scale * np.arange(q + 1)).round(precision)
    result = qcut(arr, q, precision=precision)

    for value, bucket in zip(arr, result):
        assert value in bucket

