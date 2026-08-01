
def get_nearest_alien(
    pos: int, alien_map: chex.Array
) -> Tuple[jnp.ndarray, jnp.ndarray, jnp.ndarray]:
    """Find alien closest to player in manhattan distance -> shot target."""
    ids = jnp.array([jnp.abs(jnp.array([i for i in range(10)]) - pos)])
    search_order = jnp.argsort(ids).squeeze()
    results_temp = jnp.zeros(3)
    aliens_exist = jnp.sum(alien_map, axis=0) > 0

    # Work around for np.where via element-wise multiplication with ids
    # The output has 3 dims: [alien_exists, location, id]
    counter = 0
    for i in search_order[::-1]:
        locations = alien_map[:, i] * jnp.arange(alien_map[:, i].shape[0])
        aliens_loc = jnp.max(locations)
        results_temp = (
            aliens_exist[i]
            * results_temp.at[:].set(jnp.array([aliens_exist[i], aliens_loc, i]))
            + (1 - aliens_exist[i]) * results_temp
        )
        counter += 1
    results_temp = jnp.array(results_temp, dtype=int)
    # Loop over results in reverse order
    return results_temp[0], results_temp[1], results_temp[2]

