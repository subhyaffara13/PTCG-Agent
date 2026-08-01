
def _create_empty_array_text(space: Text, n: int = 1, fn=np.zeros) -> tuple[str, ...]:
    return tuple(space.characters[0] * space.min_length for _ in range(n))

