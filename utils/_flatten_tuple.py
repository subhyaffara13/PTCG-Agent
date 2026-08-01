
def _flatten_tuple(space: Tuple, x: tuple[Any, ...]) -> tuple[Any, ...] | NDArray[Any]:
    if space.is_np_flattenable:
        return np.concatenate(
            [np.array(flatten(s, x_part)) for x_part, s in zip(x, space.spaces)]
        )
    return tuple(flatten(s, x_part) for x_part, s in zip(x, space.spaces))


def _flatten_tuple(space, x) -> Union[tuple, np.ndarray]:
    if space.is_np_flattenable:
        return np.concatenate(
            [flatten(s, x_part) for x_part, s in zip(x, space.spaces)]
        )
    return tuple(flatten(s, x_part) for x_part, s in zip(x, space.spaces))

