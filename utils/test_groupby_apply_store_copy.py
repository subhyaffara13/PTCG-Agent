
def test_groupby_apply_store_copy():
    # GH40673
    rng = np.random.default_rng(seed=42)

    df = DataFrame(
        {
            "A": rng.normal(10, 12, size=(4,)),
            "B": [1, 2, 1, 2],
        }
    )

    store = {}

    def addstore(x):
        store[len(store)] = x.copy()

    df.groupby("B").apply(addstore)

    expected_out_0 = df.iloc[[0, 2], [0]]
    expected_out_1 = df.iloc[[1, 3], [0]]

    tm.assert_frame_equal(store[0], expected_out_0)
    tm.assert_frame_equal(store[1], expected_out_1)

