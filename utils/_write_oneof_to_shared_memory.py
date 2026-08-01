
def _write_oneof_to_shared_memory(
    space: OneOf, index: int, values: tuple[int, Any], shared_memory
):
    subspace_idx, space_value = values

    destination = np.frombuffer(shared_memory[0].get_obj(), dtype=np.int64)
    np.copyto(destination[index : index + 1], subspace_idx)

    # only the subspace's memory is updated with the sample value, ignoring the other memories as data might not match
    write_to_shared_memory(
        space.spaces[subspace_idx], index, space_value, shared_memory[1 + subspace_idx]
    )

