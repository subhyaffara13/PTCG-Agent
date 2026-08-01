
def vals(n):
    vals = [
        np.random.default_rng(2).integers(0, 10, n),
        np.random.default_rng(2).choice(list("abcdefghij"), n),
        np.random.default_rng(2).choice(
            pd.date_range("20141009", periods=10).tolist(), n
        ),
        np.random.default_rng(2).choice(list("ZYXWVUTSRQ"), n),
        np.random.default_rng(2).standard_normal(n),
    ]
    vals = list(map(tuple, zip(*vals)))
    return vals

