
def serialize_env_actions(env_actions: list):
    def serialize_array(arr, key_path: str = ""):
        if isinstance(arr, np.ndarray):
            return arr.tolist()
        elif isinstance(arr, jnp.ndarray):
            return arr.tolist()
        elif isinstance(arr, dict):
            ret = dict()
            for k, v in arr.items():
                new_key = key_path + "/" + k if key_path else k
                new_val = serialize_array(v, new_key)
                if new_val is not None:
                    ret[k] = new_val
            return ret

        return arr

    steps = []
    for state in env_actions:
        state = flax.serialization.to_state_dict(state)
        steps.append(serialize_array(state))

    return steps

