from typing import Any

def _partition_joint_graph_into_fw_bw(
    fx_g: torch.fx.GraphModule,
    joint_inputs: list[Any] | tuple[list[Any], list[Any]],
    inner_meta: ViewAndMutationMeta,
    fw_metadata: ViewAndMutationMeta,
    aot_config: AOTConfig,
) -> tuple[torch.fx.GraphModule, torch.fx.GraphModule, int]:
    # See Note: [Partitioner handling for Subclasses, Part 1]
    # See Note: [Recomputing subclass mutation handling]
    mutated_inp_runtime_indices = compute_inner_mutated_inp_indices_from_subclass_meta(
        fw_metadata, inner_meta
    )
    num_tokens = len(fw_metadata.tokens)
    num_inner_fwd_outputs = (
        len(mutated_inp_runtime_indices)
        + inner_meta.num_outputs
        + inner_meta.num_intermediate_bases
        + inner_meta.num_outputs_rng_offset
        + num_tokens  # See Note [Side-Effectful Tokens in AOTAutograd]
    )

    fx_g = run_joint_graph_passes_on_hops(fx_g, joint_inputs, aot_config)

    # apply joint_gm callback here
    if callable(torch._functorch.config.joint_custom_pass):
        # pyrefly: ignore [bad-assignment]
        fx_g = torch._functorch.config.joint_custom_pass(fx_g, joint_inputs)

    if aot_config.partition_fn is None:
        raise AssertionError("aot_config.partition_fn must not be None")
    fw_module, bw_module = aot_config.partition_fn(
        fx_g,
        joint_inputs,
        num_fwd_outputs=num_inner_fwd_outputs,
        static_lifetime_input_indices=fw_metadata.static_input_indices,
    )

    rng_states = [
        n
        for n in fw_module.graph.find_nodes(op="placeholder")
        if "fwd_rng_state" in n.name
    ]
    fw_metadata.num_graphsafe_rng_states = len(rng_states)
    if rng_states:
        fw_metadata.graphsafe_rng_state_index = rng_states[0].meta["val"].device.index

    return fw_module, bw_module, num_inner_fwd_outputs

