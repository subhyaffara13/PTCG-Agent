
def align_inputs_from_check_idxs(
    model: Callable[[list[InputType]], _T],
    inputs_to_check: Sequence[int],
    mutated_input_idxs: OrderedSet[int],
) -> Callable[[list[InputType]], _T]:
    if len(inputs_to_check) == 0:
        return model

    def run(new_inputs: list[InputType]) -> Any:
        old_tensors, new_tensors = copy_misaligned_inputs(
            new_inputs, inputs_to_check, mutated_input_idxs
        )
        out = model(new_inputs)

        # If a mutated tensor was cloned to be aligned, we need to reflect back the mutation to the
        # original tensor.
        if len(old_tensors):
            torch._foreach_copy_(old_tensors, new_tensors)

        return out

    return run

