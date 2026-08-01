
def test_cut_no_warnings():
    df = DataFrame({"value": np.random.default_rng(2).integers(0, 100, 20)})
    labels = [f"{i} - {i + 9}" for i in range(0, 100, 10)]
    with tm.assert_produces_warning(False):
        df["group"] = cut(df.value, range(0, 105, 10), right=False, labels=labels)

