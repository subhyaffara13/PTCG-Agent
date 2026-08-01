
def autograd_key(
    fw_gm: GraphModule,
    *args: Any,
    **kwargs: Any,
) -> Any:
    local_map_kwargs = fw_gm.meta["local_map_kwargs"]  # type: ignore[attr-defined]
    if local_map_kwargs.get("in_grad_placements", None) is not None:
        raise AssertionError("local_map in_grad_placements are not yet supported.")
    if _DEFER_INLINING:
        fw_gm, bw_gm, num_fw_ins, num_fw_outs, filtered_grads_idx = create_hop_fw_bw(
            fw_gm, *args
        )
        return LocalMapAutogradOp.apply(
            fw_gm, bw_gm, num_fw_ins, num_fw_outs, filtered_grads_idx, *args, **kwargs
        )

    # TODO: get rid of this when we can install as a subgraph
    return torch.fx.Interpreter(fw_gm).run(*args, **kwargs)

