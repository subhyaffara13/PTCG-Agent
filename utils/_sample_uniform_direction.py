
def _sample_uniform_direction(dim, size, random_state):
    """
    Private method to generate uniform directions
    Reference: Marsaglia, G. (1972). "Choosing a Point from the Surface of a
               Sphere". Annals of Mathematical Statistics. 43 (2): 645-646.
    """
    samples_shape = np.append(size, dim)
    samples = random_state.standard_normal(samples_shape)
    samples /= np.linalg.norm(samples, axis=-1, keepdims=True)
    return samples

