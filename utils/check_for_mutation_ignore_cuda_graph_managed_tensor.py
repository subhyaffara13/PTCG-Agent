
def check_for_mutation_ignore_cuda_graph_managed_tensor(
    gm: torch.fx.GraphModule,
    mutated_inputs: OrderedSet[str],
    mutated_input_idxs: OrderedSet[int],
    static_input_idxs: Sequence[int],
) -> str | None:
    default_msg = format_default_skip_message("mutated inputs")

    # doesn't work for non-trees because the warmup run would apply mutation twice
    if torch._inductor.config.triton.cudagraph_trees:
        unique_idxs = OrderedSet(static_input_idxs)
        # checking if mutation is only on parameters/static inputs
        mutation_indices = [idx for idx in mutated_input_idxs if idx not in unique_idxs]
        has_mutation = len(mutation_indices) != 0
        if not has_mutation:
            return None
        placeholders = get_placeholder_info(gm.graph)
        return get_mutation_stack_trace(placeholders, mutation_indices)

    else:
        has_mutation = len(mutated_inputs) != 0
        return None if not has_mutation else default_msg


def check_for_mutation_ignore_cuda_graph_managed_tensor(
    aot_model: torch.fx.GraphModule, num_fixed: int
) -> str | None:
    mutation_indices = find_input_mutations(aot_model.graph) - set(range(num_fixed))
    if not mutation_indices:
        return None

    placeholders = get_placeholder_info(aot_model.graph)
    return get_mutation_stack_trace(placeholders, mutation_indices)

