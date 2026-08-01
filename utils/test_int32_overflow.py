
def test_int32_overflow():
    B = np.concatenate((np.arange(10000), np.arange(10000), np.arange(5000)))
    A = np.arange(25000)
    df = DataFrame(
        {
            "A": A,
            "B": B,
            "C": A,
            "D": B,
            "E": np.random.default_rng(2).standard_normal(25000),
        }
    )

    left = df.groupby(["A", "B", "C", "D"]).sum()
    right = df.groupby(["D", "C", "B", "A"]).sum()
    assert len(left) == len(right)

