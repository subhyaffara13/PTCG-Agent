from typing import Dict

def _jnp2np(jnp_dict: Dict[str, Array]) -> Dict[str, np.array]:
    for k, v in jnp_dict.items():
        jnp_dict[k] = np.asarray(v)
    return jnp_dict

