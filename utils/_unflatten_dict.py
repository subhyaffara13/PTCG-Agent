
def _unflatten_dict(space: Dict, x: NDArray[Any] | dict[str, Any]) -> dict[str, Any]:
    if space.is_np_flattenable:
        dims = np.asarray([flatdim(s) for s in space.spaces.values()], dtype=np.int_)
        list_flattened = np.split(x, np.cumsum(dims[:-1]))
        return {
            key: unflatten(s, flattened)
            for flattened, (key, s) in zip(list_flattened, space.spaces.items())
        }

    assert isinstance(
        x, dict
    ), f"{space} is not numpy-flattenable. Thus, you should only unflatten dictionary for this space. Got a {type(x)}"
    return {key: unflatten(s, x[key]) for key, s in space.spaces.items()}


def _unflatten_dict(space: Dict, x: Union[np.ndarray, TypingDict]) -> dict:
    if space.is_np_flattenable:
        dims = np.asarray([flatdim(s) for s in space.spaces.values()], dtype=np.int_)
        list_flattened = np.split(x, np.cumsum(dims[:-1]))
        return OrderedDict(
            [
                (key, unflatten(s, flattened))
                for flattened, (key, s) in zip(list_flattened, space.spaces.items())
            ]
        )
    assert isinstance(
        x, dict
    ), f"{space} is not numpy-flattenable. Thus, you should only unflatten dictionary for this space. Got a {type(x)}"
    return OrderedDict((key, unflatten(s, x[key])) for key, s in space.spaces.items())

