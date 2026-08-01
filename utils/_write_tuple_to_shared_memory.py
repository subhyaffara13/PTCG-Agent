
def _write_tuple_to_shared_memory(
    space: Tuple, index: int, values: tuple[Any, ...], shared_memory
):
    for value, memory, subspace in zip(values, shared_memory, space.spaces):
        write_to_shared_memory(subspace, index, value, memory)


def _write_tuple_to_shared_memory(space, index, values, shared_memory):
    for value, memory, subspace in zip(values, shared_memory, space.spaces):
        write_to_shared_memory(subspace, index, value, memory)

