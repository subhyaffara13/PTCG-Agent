
def test_findlike_promoters():
    r = "Wally"
    l = "Where's Wally?"
    s = np.int32(3)
    e = np.int8(13)
    for dtypes in [("T", "U"), ("U", "T")]:
        for function, answer in [
            (np.strings.index, 8),
            (np.strings.endswith, True),
        ]:
            assert answer == function(
                np.array(l, dtype=dtypes[0]), np.array(r, dtype=dtypes[1]), s, e
            )

