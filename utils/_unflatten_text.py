
def _unflatten_text(space: Text, x: NDArray[np.int32]) -> str:
    return "".join(
        [space.character_list[val] for val in x if val < len(space.character_set)]
    )


def _unflatten_text(space: Text, x: np.ndarray) -> str:
    return "".join(
        [space.character_list[val] for val in x if val < len(space.character_set)]
    )

