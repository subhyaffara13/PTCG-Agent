
def test_apply_without_copy():
    # GH 5545
    # returning a non-copy in an applied function fails

    data = DataFrame(
        {
            "id_field": [100, 100, 200, 300],
            "category": ["a", "b", "c", "c"],
            "value": [1, 2, 3, 4],
        }
    )

    def filt1(x):
        if x.shape[0] == 1:
            return x.copy()
        else:
            return x[x.category == "c"]

    def filt2(x):
        if x.shape[0] == 1:
            return x
        else:
            return x[x.category == "c"]

    expected = data.groupby("id_field").apply(filt1)
    result = data.groupby("id_field").apply(filt2)
    tm.assert_frame_equal(result, expected)

