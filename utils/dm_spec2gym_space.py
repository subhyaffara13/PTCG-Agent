
def dm_spec2gym_space(spec) -> spaces.Space[Any]:
    """Converts a dm_env spec to a gymnasium space."""
    if isinstance(spec, (OrderedDict, dict)):
        return spaces.Dict(
            {key: dm_spec2gym_space(value) for key, value in copy.copy(spec).items()}
        )
    # not possible to use isinstance due to inheritance
    elif type(spec) is BoundedArray:
        low = np.broadcast_to(spec.minimum, spec.shape)
        high = np.broadcast_to(spec.maximum, spec.shape)
        return spaces.Box(
            low=low,
            high=high,
            shape=spec.shape,
            dtype=spec.dtype,  # pyright: ignore[reportGeneralTypeIssues]
        )
    elif type(spec) is Array:
        if np.issubdtype(spec.dtype, np.integer):
            low = np.iinfo(spec.dtype).min
            high = np.iinfo(spec.dtype).max
        elif np.issubdtype(spec.dtype, np.inexact):
            low = float("-inf")
            high = float("inf")
        elif spec.dtype == "bool":
            low = int(0)
            high = int(1)
        else:
            raise TypeError(f"Unknown dtype {spec.dtype} for spec {spec}.")

        return spaces.Box(
            low=low,
            high=high,
            shape=spec.shape,
            dtype=spec.dtype,  # pyright: ignore[reportGeneralTypeIssues]
        )
    elif type(spec) is DiscreteArray:
        return spaces.Discrete(spec.num_values)
    else:
        raise NotImplementedError(
            f"Cannot convert dm_spec to gymnasium space, unknown spec: {spec}, please report."
        )

