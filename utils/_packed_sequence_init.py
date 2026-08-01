
def _packed_sequence_init(
    data: Tensor,
    batch_sizes: Tensor | None = None,
    sorted_indices: Tensor | None = None,
    unsorted_indices: Tensor | None = None,
) -> PackedSequence:
    data, batch_sizes, sorted_indices, unsorted_indices = _packed_sequence_init_args(
        data, batch_sizes, sorted_indices, unsorted_indices
    )
    return PackedSequence(data, batch_sizes, sorted_indices, unsorted_indices)

