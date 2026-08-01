
def _fixed_default_rng(seed=1638083107694713882823079058616272161):
    """Context with a fixed np.random.default_rng seed."""
    orig_fun = np.random.default_rng
    np.random.default_rng = lambda seed=seed: orig_fun(seed)
    try:
        yield
    finally:
        np.random.default_rng = orig_fun

