
def copy_misaligned_inputs(
    new_inputs: list[InputType],
    check_inputs_idxs: Sequence[int],
    return_pair_idxs: OrderedSet[int] | None = None,
) -> tuple[list[torch.Tensor], list[torch.Tensor]]:
    """
    Clones misaligned tensors which we inferred were aligned. Returns a tuple of [old_tensors], [new_tensors] for every
    cloned tensor which is in `return_pair_idxs`.
    """

    old_tensors: list[torch.Tensor] = []
    new_tensors: list[torch.Tensor] = []

    # hoist above loop because this is on the hot path
    ret_pair_defined = return_pair_idxs is not None
    for i in check_inputs_idxs:
        _inp = new_inputs[i]
        assert isinstance(_inp, torch.Tensor), (
            f"Expected tensors only, but got: {type(_inp)}"
        )
        if _inp.data_ptr() % ALIGNMENT:
            new_inputs[i] = clone_preserve_strides(_inp)

            if ret_pair_defined and i in return_pair_idxs:  # type: ignore[operator]
                old_tensors.append(_inp)
                new_tensors.append(new_inputs[i])  # type: ignore[arg-type]

    return old_tensors, new_tensors

