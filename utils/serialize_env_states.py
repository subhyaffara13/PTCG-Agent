
def serialize_env_states(env_states: list[EnvState]):
    def serialize_array(root: EnvState, arr, key_path: str = ""):
        if key_path in [
            "sensor_mask",
            "relic_nodes_mask",
            "energy_nodes_mask",
            "energy_node_fns",
            "relic_nodes_map_weights",
            "relic_spawn_schedule",
        ]:
            return None
        if key_path == "relic_nodes":
            return root.relic_nodes[root.relic_nodes_mask].tolist()
        if key_path == "relic_node_configs":
            return root.relic_node_configs[root.relic_nodes_mask].tolist()
        if key_path == "energy_nodes":
            return root.energy_nodes[root.energy_nodes_mask].tolist()
        if isinstance(arr, jnp.ndarray):
            return arr.tolist()
        elif isinstance(arr, dict):
            ret = dict()
            for k, v in arr.items():
                new_key = key_path + "/" + k if key_path else k
                new_val = serialize_array(root, v, new_key)
                if new_val is not None:
                    ret[k] = new_val
            return ret
        return arr

    steps = []
    for state in env_states:
        state_dict = flax.serialization.to_state_dict(state)
        steps.append(serialize_array(state, state_dict))

    return steps

