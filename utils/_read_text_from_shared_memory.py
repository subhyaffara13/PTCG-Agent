
def _read_text_from_shared_memory(
    space: Text, shared_memory, n: int = 1
) -> tuple[str, ...]:
    data = np.frombuffer(shared_memory.get_obj(), dtype=np.int32).reshape(
        (n, space.max_length)
    )

    return tuple(
        "".join(
            [
                space.character_list[val]
                for val in values
                if val < len(space.character_set)
            ]
        )
        for values in data
    )

