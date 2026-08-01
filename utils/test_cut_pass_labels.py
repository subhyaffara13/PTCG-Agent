
def test_cut_pass_labels(get_labels, get_expected):
    bins = [0, 25, 50, 100]
    arr = [50, 5, 10, 15, 20, 30, 70]
    labels = ["Small", "Medium", "Large"]

    result = cut(arr, bins, labels=get_labels(labels))
    tm.assert_categorical_equal(result, get_expected(labels))

