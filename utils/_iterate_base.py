
def _iterate_base(space: Box | MultiDiscrete | MultiBinary, items: np.ndarray):
    try:
        return iter(items)
    except TypeError as e:
        raise TypeError(
            f"Unable to iterate over the following elements: {items}"
        ) from e


def _iterate_base(space, items):
    try:
        return iter(items)
    except TypeError:
        raise TypeError(f"Unable to iterate over the following elements: {items}")

