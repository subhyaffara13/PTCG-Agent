
def _np2jnp(numpy_dict: Dict[str, np.ndarray]) -> Dict[str, Array]:
    for k, v in numpy_dict.items():
        numpy_dict[k] = jnp.array(v)
    return numpy_dict

