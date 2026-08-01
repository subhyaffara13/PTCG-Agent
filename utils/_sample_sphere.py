
def _sample_sphere(n, dim, seed=None):
    # Sample points uniformly at random from the hypersphere
    rng = np.random.RandomState(seed=seed)
    points = rng.randn(n, dim)
    points /= np.linalg.norm(points, axis=1, keepdims=True)
    return points

