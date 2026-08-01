
def get_input_idxs_to_check(
    inputs: Sequence[InputType],
    static_input_idxs: Sequence[int],
) -> Sequence[int]:
    """
    This function runs at compile time, and generates a list of indices for which we
    might need to do a copy to preserve alignment requirements.
    """
    ids_to_check = []

    for i, input in enumerate(inputs):
        if not isinstance(input, torch.Tensor):
            # non-tensors don't need alignment
            continue
        if not is_gpu(input.device.type):
            # right now we only care for gpu tensors
            continue
        with maybe_get_suppress_shape_guards_ctx():
            # suppress guards so that tensor_is_aligned and should_assume_input_aligned
            # do not add guards on input's storage offset
            if i in static_input_idxs and tensor_is_aligned(input):
                continue
            if not should_assume_input_aligned(input):
                continue

        # if we get here, then
        # (a) our triton code assumes that the input is aligned
        # (b) we can't be sure ahead of time that the input will actually be aligned.
        # therefore, at runtime, we'll need to check that the input is aligned
        # (and if not, clone it to make it aligned.)
        ids_to_check.append(i)

    return ids_to_check

