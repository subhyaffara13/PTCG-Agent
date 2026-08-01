
def angle_normalize(x: jnp.ndarray) -> jnp.ndarray:
    """Normalize the angle - radians."""
    return ((x + jnp.pi) % (2 * jnp.pi)) - jnp.pi


def angle_normalize(x):
    return ((x + np.pi) % (2 * np.pi)) - np.pi


def angle_normalize(x):
    return ((x + np.pi) % (2 * np.pi)) - np.pi

