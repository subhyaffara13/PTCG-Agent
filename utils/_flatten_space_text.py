
def _flatten_space_text(space: Text) -> Box:
    return Box(
        low=0, high=len(space.character_set), shape=(space.max_length,), dtype=np.int32
    )


def _flatten_space_text(space: Text) -> Box:
    return Box(
        low=0, high=len(space.character_set), shape=(space.max_length,), dtype=np.int32
    )

