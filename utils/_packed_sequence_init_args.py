
def _packed_sequence_init_args(
    data: Tensor,
    batch_sizes: Tensor | None = None,
    sorted_indices: Tensor | None = None,
    unsorted_indices: Tensor | None = None,
) -> tuple[Tensor, Tensor, Tensor | None, Tensor | None]:
    # NB: if unsorted_indices is provided, it should be the inverse permutation
    # to sorted_indices. Don't assert it here because the PackedSequence ctor
    # should only be used internally.

    if unsorted_indices is None:
        unsorted_indices = invert_permutation(sorted_indices)

    # support being called as `PackedSequence(data, batch_sizes, sorted_indices)`
    if batch_sizes is not None:
        # TODO: Re-enable this check (.type isn't supported in TorchScript)
        if batch_sizes.device.type != "cpu":
            raise ValueError(
                "batch_sizes should always be on CPU. "
                "Instances of PackedSequence should never be created manually. "
                "They should be instantiated by functions like pack_sequence "
                "and pack_padded_sequences in nn.utils.rnn. "
                "https://pytorch.org/docs/stable/nn.html#torch.nn.utils.rnn.pack_sequence"
            )
        return data, batch_sizes, sorted_indices, unsorted_indices

    # support being called as `PackedSequence((data, batch_sizes), *, sorted_indices)`
    else:
        if not (isinstance(data, (list, tuple)) and len(data) == 2):
            raise AssertionError("Expected data to be a list or tuple of length 2")
        return data[0], data[1], sorted_indices, unsorted_indices

