
def _integer_integers(_integer):
    # integers to get a case with zeros
    return _integer * np.random.default_rng(2).integers(0, 2, size=np.shape(_integer))

