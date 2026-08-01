
def apply_graphsafe_rng_functionalization(
    fw_module: torch.fx.GraphModule,
    bw_module: torch.fx.GraphModule,
    fw_node: torch.fx.Node,
    bw_node: torch.fx.Node,
    device: torch.device,
    rng_count: int,
    last_fwd_input: torch.fx.Node,
    last_bwd_input: torch.fx.Node,
) -> tuple[torch.fx.Node, torch.fx.Node]:
    """
    Note [CUDA Graph Safe RNG Functionalization]

    CUDA Graph capture doesn't work with get_rng_state and set_rng_state because these functions operate on CPU values,
    while CUDA Graph RNG capture uses on-device CUDA tensors. To solve this, we use graphsafe_set_state with a
    CUDA Generator registered to the CUDA Graph before capture begins. graphsafe_set_state updates the generator's pointer
    to reference a different GeneratorImpl, ensuring subsequent calls are correctly forwarded to the desired generator
    (and its cuda-tensor RNG state during graph capture).

    For each RNG operation's forward/backward pair:

    - We create two generators initialized with identical values
    - Each forward and backward call advances its respective generator equally
    - This keeps generators synchronized so forward and backward operations use matching RNG values

    When forward is called multiple times before backward (causing desynchronization):

    - We save the forward RNG state
    - We update the backward Generator's state before executing backward

    Before each CUDA Graph replay, replay_prologue updates captured RNG pointers with current states, ensuring backward Generator
    changes are reflected during replay.

    This function modifies both forward and backward computation graphs by:

    Creating RNG state placeholders for both passes
    Updating the forward node to use graph-safe RNG state
    Updating the backward node to use graph-safe RNG state

    For more details: https://github.com/pytorch/pytorch/issues/113541
    """
    device_idx = device.index
    if device_idx is None:
        raise AssertionError("device_idx must not be None")
    fw_graph = fw_module.graph
    bw_graph = bw_module.graph
    graphsafe_run_with_rng_state = torch._prims.rng_prims.graphsafe_run_with_rng_state

    # Handle forward pass

    # Note: [Generator arguments in AOTDispatcher]
    # Generator arguments in AOTDispatcher are added to support graphsafe rng
    # functionalization. See note above [CUDA Graph Safe RNG Functionalization]
    with fw_module.graph.inserting_after(last_fwd_input):
        fwd_rng_state = fw_module.graph.placeholder(f"fwd_rng_state_{rng_count}")
        fwd_rng_state.meta["val"] = get_cuda_generator_meta_val(device_idx)
        last_fwd_input = fwd_rng_state

    # Handle backward pass
    with bw_module.graph.inserting_after(last_bwd_input):
        bwd_rng_state = bw_module.graph.placeholder(f"bwd_rng_state_{rng_count}")
        # as above, clone so that meta val generator will not contain tensors
        bwd_rng_state.meta["val"] = get_cuda_generator_meta_val(device_idx)
        last_bwd_input = bwd_rng_state

    # Update forward node
    fw_kwargs = dict(fw_node.kwargs)
    fw_kwargs["rng_state"] = fwd_rng_state
    with fw_module.graph.inserting_after(fw_node):
        functional_fw_node = fw_graph.create_node(
            "call_function",
            graphsafe_run_with_rng_state,
            args=(fw_node.target, *fw_node.args),  # type: ignore[arg-type]
            kwargs=fw_kwargs,
        )
    fw_node.replace_all_uses_with(functional_fw_node)
    fw_graph.erase_node(fw_node)

    # Update backward node
    bwd_kwargs = dict(bw_node.kwargs)
    bwd_kwargs["rng_state"] = bwd_rng_state
    with bw_graph.inserting_before(bw_node):
        rng_output = bw_graph.create_node(
            "call_function",
            graphsafe_run_with_rng_state,
            args=(bw_node.target, *bw_node.args),  # type: ignore[arg-type]
            kwargs=bwd_kwargs,
        )
        bw_node.replace_all_uses_with(rng_output)
        bw_graph.erase_node(bw_node)

    return last_fwd_input, last_bwd_input

