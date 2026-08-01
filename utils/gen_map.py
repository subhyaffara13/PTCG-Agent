
def gen_map(
    xs,
    ys,
    n_obs,
    randomizer,
    center_bounds=[0.0, 1.0],
    length_bounds=[0.1, 0.5],
    gmap=None,
):
    cl, cu = center_bounds
    ll, lu = length_bounds
    if gmap is None:
        gmap = np.zeros((xs, ys), dtype=np.int32)
    for _ in range(n_obs):
        xc = randomizer.uniform(cl, cu)
        yc = randomizer.uniform(cl, cu)
        xl = randomizer.uniform(ll, lu)
        yl = randomizer.uniform(ll, lu)
        gmap = add_rectangle(gmap, xc=xc, yc=yc, xl=xl, yl=yl)
    return gmap


def gen_map(
    key: chex.PRNGKey,
    params: EnvParams,
    map_type: int,
    map_height: int,
    map_width: int,
    max_energy_nodes: int,
    max_relic_nodes: int,
    relic_config_size: int,
) -> chex.Array:
    map_features = MapTile(
        energy=jnp.zeros(shape=(map_height, map_width), dtype=jnp.int16),
        tile_type=jnp.zeros(shape=(map_height, map_width), dtype=jnp.int16),
    )
    energy_nodes = jnp.zeros(shape=(max_energy_nodes, 2), dtype=jnp.int16)
    energy_nodes_mask = jnp.zeros(shape=(max_energy_nodes), dtype=jnp.bool)
    relic_nodes = jnp.zeros(shape=(max_relic_nodes, 2), dtype=jnp.int16)
    relic_nodes_mask = jnp.zeros(shape=(max_relic_nodes), dtype=jnp.bool)

    if MAP_TYPES[map_type] == "random":
        ### Generate nebula tiles ###
        key, subkey = jax.random.split(key)
        perlin_noise = generate_perlin_noise_2d(subkey, (map_height, map_width), (4, 4))
        noise = jnp.where(perlin_noise > 0.5, 1, 0)
        # mirror along diagonal
        noise = noise | noise.T
        noise = noise[::-1, ::1]
        map_features = map_features.replace(tile_type=jnp.where(noise, NEBULA_TILE, 0))

        ### Generate asteroid tiles ###
        key, subkey = jax.random.split(key)
        perlin_noise = generate_perlin_noise_2d(subkey, (map_height, map_width), (8, 8))
        noise = jnp.where(perlin_noise < -0.5, 1, 0)
        # mirror along diagonal
        noise = noise | noise.T
        noise = noise[::-1, ::1]
        map_features = map_features.replace(
            tile_type=jnp.place(map_features.tile_type, noise, ASTEROID_TILE, inplace=False)
        )

        ### Generate relic nodes ###
        key, subkey = jax.random.split(key)
        noise = generate_perlin_noise_2d(subkey, (map_height, map_width), (4, 4))
        # Find the positions of the  highest noise values
        flat_indices = jnp.argsort(noise.ravel())[-max_relic_nodes // 2 :]  # Get indices of two highest values
        highest_positions = jnp.column_stack(jnp.unravel_index(flat_indices, noise.shape))

        # relic nodes have a fixed density of 20% nearby tiles can yield points
        relic_node_configs = (
            jax.random.randint(
                key,
                shape=(
                    max_relic_nodes,
                    relic_config_size,
                    relic_config_size,
                ),
                minval=0,
                maxval=10,
            ).astype(jnp.float32)
            >= 7.5
        )
        highest_positions = highest_positions.astype(jnp.int16)
        mirrored_positions = jnp.stack(
            [map_width - highest_positions[:, 1] - 1, map_height - highest_positions[:, 0] - 1],
            dtype=jnp.int16,
            axis=-1,
        )
        relic_nodes = jnp.concat([highest_positions, mirrored_positions], axis=0)

        key, subkey = jax.random.split(key)
        num_spawned_relic_nodes = jax.random.randint(key, (1,), minval=1, maxval=(max_relic_nodes // 2) + 1)
        relic_nodes_mask_half = jnp.arange(max_relic_nodes // 2) < num_spawned_relic_nodes
        relic_nodes_mask = jnp.concat([relic_nodes_mask_half, relic_nodes_mask_half], axis=0)
        relic_node_configs = relic_node_configs.at[max_relic_nodes // 2 :].set(
            relic_node_configs[: max_relic_nodes // 2].transpose(0, 2, 1)[:, ::-1, ::-1]
        )
        # note that relic nodes mask is always increasing.

        ### Generate energy nodes ###
        key, subkey = jax.random.split(key)
        noise = generate_perlin_noise_2d(subkey, (map_height, map_width), (4, 4))
        # Find the positions of the  highest noise values
        flat_indices = jnp.argsort(noise.ravel())[-max_energy_nodes // 2 :]  # Get indices of highest values
        highest_positions = jnp.column_stack(jnp.unravel_index(flat_indices, noise.shape)).astype(jnp.int16)
        mirrored_positions = jnp.stack(
            [map_width - highest_positions[:, 1] - 1, map_height - highest_positions[:, 0] - 1],
            dtype=jnp.int16,
            axis=-1,
        )
        energy_nodes = jnp.concat([highest_positions, mirrored_positions], axis=0)
        key, subkey = jax.random.split(key)
        energy_nodes_mask_half = jax.random.randint(key, (max_energy_nodes // 2,), minval=0, maxval=2).astype(jnp.bool)
        energy_nodes_mask_half = energy_nodes_mask_half.at[0].set(True)
        energy_nodes_mask = energy_nodes_mask.at[: max_energy_nodes // 2].set(energy_nodes_mask_half)
        energy_nodes_mask = energy_nodes_mask.at[max_energy_nodes // 2 :].set(energy_nodes_mask_half)

        energy_node_fns = jnp.array(
            [
                [0, 1.2, 1, 4],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                # [1, 4, 0, 2],
                [0, 1.2, 1, 4],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                # [1, 4, 0, 0]
            ]
        )

        # generate a random relic spawn schedule
        # if number is -1, then relic node is never spawned, otherwise spawn at that game timestep
        assert max_relic_nodes == 6, "random map generation is hardcoded to use 6 relic nodes at most per map"
        key, subkey = jax.random.split(key)
        relic_spawn_schedule_half = jax.random.randint(
            key, (max_relic_nodes // 2,), minval=0, maxval=params.max_steps_in_match // 2
        ) + jnp.arange(3) * (params.max_steps_in_match + 1)
        relic_spawn_schedule = jnp.concat([relic_spawn_schedule_half, relic_spawn_schedule_half], axis=0)
        relic_spawn_schedule = jnp.where(relic_nodes_mask, relic_spawn_schedule, -1)

    return dict(
        map_features=map_features,
        energy_nodes=energy_nodes,
        energy_node_fns=energy_node_fns,
        relic_nodes=relic_nodes,
        energy_nodes_mask=energy_nodes_mask,
        relic_nodes_mask=relic_nodes_mask,
        relic_node_configs=relic_node_configs,
        relic_spawn_schedule=relic_spawn_schedule,
    )

