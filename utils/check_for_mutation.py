
def check_for_mutation(
    func: WrappedFunction,
    inputs: list[InputType],
    is_cuda_graph_recorded_tensor: Callable[[torch.Tensor], bool],
) -> str | None:
    # doesn't work for non-trees because the warmup run would apply mutation twice
    if torch._inductor.config.triton.cudagraph_trees:
        # checking if mutation is only on parameters/static inputs
        mutation_indices: Sequence[int] = [
            idx
            for idx in func.mutated_input_idxs
            if not (
                idx in func.static_input_idxs
                or is_cuda_graph_recorded_tensor(inputs[idx])  # type: ignore[arg-type]
            )
        ]
    else:
        mutation_indices = func.mutated_input_idxs

    static_inputs_log.debug(
        "check mutation static input indices: %s", func.static_input_idxs
    )
    static_inputs_log.debug("check mutation mutation indices: %s", mutation_indices)

    return (
        get_mutation_stack_trace(func.placeholders, mutation_indices)
        if mutation_indices
        else None
    )

