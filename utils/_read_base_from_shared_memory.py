
def _read_base_from_shared_memory(
    space: Box | Discrete | MultiDiscrete | MultiBinary, shared_memory, n: int = 1
):
    return np.frombuffer(shared_memory.get_obj(), dtype=space.dtype).reshape(
        (n,) + space.shape
    )


def _read_base_from_shared_memory(space, shared_memory, n: int = 1):
    return np.frombuffer(shared_memory.get_obj(), dtype=space.dtype).reshape(
        (n,) + space.shape
    )

