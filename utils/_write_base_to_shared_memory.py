
def _write_base_to_shared_memory(
    space: Box | Discrete | MultiDiscrete | MultiBinary,
    index: int,
    value,
    shared_memory,
):
    size = int(np.prod(space.shape))
    destination = np.frombuffer(shared_memory.get_obj(), dtype=space.dtype)
    np.copyto(
        destination[index * size : (index + 1) * size],
        np.asarray(value, dtype=space.dtype).flatten(),
    )


def _write_base_to_shared_memory(space, index, value, shared_memory):
    size = int(np.prod(space.shape))
    destination = np.frombuffer(shared_memory.get_obj(), dtype=space.dtype)
    np.copyto(
        destination[index * size : (index + 1) * size],
        np.asarray(value, dtype=space.dtype).flatten(),
    )

