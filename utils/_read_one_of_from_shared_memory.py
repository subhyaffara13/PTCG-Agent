
def _read_one_of_from_shared_memory(
    space: OneOf, shared_memory, n: int = 1
) -> tuple[Any, ...]:
    sample_indexes = np.frombuffer(shared_memory[0].get_obj(), dtype=np.int64)

    subspace_samples = tuple(
        read_from_shared_memory(subspace, memory, n=n)
        for (memory, subspace) in zip(shared_memory[1:], space.spaces)
    )
    return tuple(
        (sample_index, subspace_samples[sample_index][index])
        for index, sample_index in enumerate(sample_indexes)
    )

