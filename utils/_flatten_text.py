
def _flatten_text(space: Text, x: str) -> NDArray[np.int32]:
    arr = np.full(
        shape=(space.max_length,), fill_value=len(space.character_set), dtype=np.int32
    )
    for i, val in enumerate(x):
        arr[i] = space.character_index(val)
    return arr


def _flatten_text(space: Text, x: str) -> np.ndarray:
    arr = np.full(
        shape=(space.max_length,), fill_value=len(space.character_set), dtype=np.int32
    )
    for i, val in enumerate(x):
        arr[i] = space.character_index(val)
    return arr

