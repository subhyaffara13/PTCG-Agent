
def _write_text_to_shared_memory(space: Text, index: int, values: str, shared_memory):
    size = space.max_length
    destination = np.frombuffer(shared_memory.get_obj(), dtype=np.int32)
    np.copyto(
        destination[index * size : (index + 1) * size],
        flatten(space, values),
    )

