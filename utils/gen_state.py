
def gen_state(
    key: chex.PRNGKey,
    env_params: EnvParams,
    max_units: int,
    num_teams: int,
    map_type: int,
    map_width: int,
    map_height: int,
    max_energy_nodes: int,
    max_relic_nodes: int,
    relic_config_size: int,
) -> EnvState:
    generated = gen_map(
        key, env_params, map_type, map_width, map_height, max_energy_nodes, max_relic_nodes, relic_config_size
    )
    relic_nodes_map_weights = jnp.zeros(shape=(map_width, map_height), dtype=jnp.int16)

    # TODO (this could be optimized better)
    def update_relic_node(relic_nodes_map_weights, relic_data):
        relic_node, relic_node_config, mask, relic_node_id = relic_data
        start_y = relic_node[1] - relic_config_size // 2
        start_x = relic_node[0] - relic_config_size // 2

        for dy in range(relic_config_size):
            for dx in range(relic_config_size):
                y, x = start_y + dy, start_x + dx
                valid_pos = jnp.logical_and(
                    jnp.logical_and(y >= 0, x >= 0),
                    jnp.logical_and(y < map_height, x < map_width),
                )
                # ensure we don't override previous spawns
                has_points = jnp.logical_and(relic_nodes_map_weights > 0, relic_nodes_map_weights <= relic_node_id + 1)
                relic_nodes_map_weights = jnp.where(
                    valid_pos & mask & jnp.logical_not(has_points) & relic_node_config[dx, dy],
                    relic_nodes_map_weights.at[x, y].set(
                        relic_node_config[dx, dy].astype(jnp.int16) * (relic_node_id + 1)
                    ),
                    relic_nodes_map_weights,
                )
        return relic_nodes_map_weights, None

    # this is really slow...

    relic_nodes_map_weights, _ = jax.lax.scan(
        update_relic_node,
        relic_nodes_map_weights,
        (
            generated["relic_nodes"],
            generated["relic_node_configs"],
            generated["relic_nodes_mask"],
            jnp.arange(max_relic_nodes, dtype=jnp.int16) % (max_relic_nodes // 2),
        ),
    )

    state = EnvState(
        units=UnitState(
            position=jnp.zeros(shape=(num_teams, max_units, 2), dtype=jnp.int16),
            energy=jnp.zeros(shape=(num_teams, max_units, 1), dtype=jnp.int16),
        ),
        units_mask=jnp.zeros(shape=(num_teams, max_units), dtype=jnp.bool),
        team_points=jnp.zeros(shape=(num_teams), dtype=jnp.int32),
        team_wins=jnp.zeros(shape=(num_teams), dtype=jnp.int32),
        energy_nodes=generated["energy_nodes"],
        energy_node_fns=generated["energy_node_fns"],
        energy_nodes_mask=generated["energy_nodes_mask"],
        # energy_field=jnp.zeros(shape=(params.map_height, params.map_width), dtype=jnp.int16),
        relic_nodes=generated["relic_nodes"],
        relic_nodes_mask=jnp.zeros(
            shape=(max_relic_nodes), dtype=jnp.bool
        ),  # as relic nodes are spawn in, we start with them all invisible.
        relic_node_configs=generated["relic_node_configs"],
        relic_nodes_map_weights=relic_nodes_map_weights,
        relic_spawn_schedule=generated["relic_spawn_schedule"],
        sensor_mask=jnp.zeros(
            shape=(num_teams, map_height, map_width),
            dtype=jnp.bool,
        ),
        vision_power_map=jnp.zeros(shape=(num_teams, map_height, map_width), dtype=jnp.int16),
        map_features=generated["map_features"],
    )
    return state

