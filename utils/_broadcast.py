from typing import Tuple, Union

def _broadcast(input, src, tag, ranks, group_size):
    group_name = c10d._resolve_group_name_by_ranks_and_tag(ranks, tag)
    return torch.ops._c10d_functional.broadcast(
        input,
        src,
        group_name,
    )


def _broadcast(state, planets, fleets):
    obs0 = state[0].observation
    obs0.planets = planets
    obs0.fleets = fleets
    for i in range(1, len(state)):
        state[i].observation.planets = planets
        state[i].observation.fleets = fleets


def _broadcast(
    value: Union[SupportsFloat, np.ndarray],
    dtype,
    shape: Tuple[int, ...],
    inf_sign: str,
) -> np.ndarray:
    """Handle infinite bounds and broadcast at the same time if needed."""
    if is_float_integer(value):
        value = get_inf(dtype, inf_sign) if np.isinf(value) else value  # type: ignore
        value = np.full(shape, value, dtype=dtype)
    else:
        assert isinstance(value, np.ndarray)
        if np.any(np.isinf(value)):
            # create new array with dtype, but maintain old one to preserve np.inf
            temp = value.astype(dtype)
            temp[np.isinf(value)] = get_inf(dtype, inf_sign)
            value = temp
    return value

