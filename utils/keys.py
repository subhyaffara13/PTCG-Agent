
def keys(n, m, vals):
    # bunch of keys for testing
    keys = [
        np.random.default_rng(2).integers(0, 11, m),
        np.random.default_rng(2).choice(list("abcdefghijk"), m),
        np.random.default_rng(2).choice(
            pd.date_range("20141009", periods=11).tolist(), m
        ),
        np.random.default_rng(2).choice(list("ZYXWVUTSRQP"), m),
    ]
    keys = list(map(tuple, zip(*keys)))
    keys += [t[:-1] for t in vals[:: n // m]]
    return keys


def keys():
    """Manage API keys for the LiteLLM proxy server"""
    pass

