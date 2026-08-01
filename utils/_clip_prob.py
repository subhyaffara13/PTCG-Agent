
def _clip_prob(p):
    """clips a probability to range 0<=p<=1."""
    return np.clip(p, 0.0, 1.0)

