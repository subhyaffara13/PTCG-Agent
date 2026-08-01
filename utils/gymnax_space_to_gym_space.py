
def gymnax_space_to_gym_space(space: Space) -> gspc.Space:
    """Convert Gymnax space to equivalent Gym space."""
    if isinstance(space, Discrete):
        return gspc.Discrete(space.n)
    elif isinstance(space, Box):
        low = (
            float(space.low)
            if (np.isscalar(space.low) or space.low.size == 1)
            else np.array(space.low)
        )
        high = (
            float(space.high)
            if (np.isscalar(space.high) or space.low.size == 1)
            else np.array(space.high)
        )
        return gspc.Box(low, high, space.shape, space.dtype)
    elif isinstance(space, Dict):
        return gspc.Dict({k: gymnax_space_to_gym_space(v) for k, v in space.spaces})
    elif isinstance(space, Tuple):
        return gspc.Tuple(space.spaces)
    else:
        raise NotImplementedError(
            f"Conversion of {space.__class__.__name__} not supported"
        )

