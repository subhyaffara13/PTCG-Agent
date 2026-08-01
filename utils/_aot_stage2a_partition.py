
def _aot_stage2a_partition(
    fx_g: torch.fx.GraphModule,
    joint_inputs: list[Any] | tuple[list[Any], list[Any]],
    maybe_subclass_meta: SubclassMeta | None,
    fw_metadata: ViewAndMutationMeta,
    aot_config: AOTConfig,
) -> tuple[torch.fx.GraphModule, torch.fx.GraphModule, int, int, list[int], list[Any]]:
    """
    Partition the joint graph into a forward graph and a backward graph. Returns:
    - the forward and backward graphs
    - the number of forward outputs and the number of symints saved for backward
    - indices of inputs to detach
    - adjusted inputs to forward
    """
    disable_amp = torch._C._is_any_autocast_enabled()
    inner_meta = _get_inner_meta(maybe_subclass_meta, fw_metadata)

    with torch.no_grad():
        context = torch._C._DisableAutocast if disable_amp else nullcontext
        with context(), track_graph_compiling(aot_config, "joint"):
            fw_module, bw_module, num_inner_fwd_outputs = (
                _partition_joint_graph_into_fw_bw(
                    fx_g,
                    joint_inputs,
                    inner_meta,
                    fw_metadata,
                    aot_config,
                )
            )
            num_inner_fwd_outputs, joint_inputs = (
                _maybe_unlift_partitioned_effect_tokens(
                    fw_module,
                    bw_module,
                    joint_inputs,
                    fw_metadata,
                    aot_config,
                    num_inner_fwd_outputs,
                )
            )

            maybe_inline_graph_saved_tensors_hooks(
                fw_module,
                bw_module,
                num_inner_fwd_outputs,
                inner_meta,
                aot_config,
                fw_metadata.static_input_indices,
            )
            num_fw_outs_saved_for_bw, num_symints_saved_for_bw = (
                _categorize_saved_tensors_for_backward(
                    fw_module,
                    bw_module,
                    inner_meta,
                    fw_metadata,
                    num_inner_fwd_outputs,
                )
            )

        _indices_of_inps_to_detach = _compute_indices_of_inps_to_detach(
            bw_module,
            maybe_subclass_meta,
            inner_meta,
            fw_metadata,
        )

    return (
        fw_module,
        bw_module,
        num_fw_outs_saved_for_bw,
        num_symints_saved_for_bw,
        _indices_of_inps_to_detach,
        _joint_inputs_for_forward(joint_inputs),
    )

