from typing import Any

def fake_mode_key(
    mode: FakeTensorMode,
    gm: GraphModule,
    *args: Any,
    **kwargs: Any,
) -> GraphArg:
    with mode:
        if not _DEFER_INLINING:
            return gm(*args, **kwargs)

        # otherwise, we need to convert to local shapes for AP
        is_backward = gm.meta["is_backward"]
        redistribute_inputs = (
            redistribute_bw_inputs if is_backward else redistribute_fw_inputs
        )
        local_args = redistribute_inputs(
            args,
            gm.meta["local_map_kwargs"]["in_placements"],
            gm.meta["local_map_kwargs"]["device_mesh"],
            gm.meta["num_activations"],
        )
        local_outs = gm(*local_args)
        redistribute_outputs = (
            redistribute_bw_outputs if is_backward else redistribute_fw_outputs
        )
        global_outs = redistribute_outputs(
            local_outs,
            gm.meta["local_map_kwargs"]["out_placements"],
            gm.meta["local_map_kwargs"]["device_mesh"],
            gm.meta["num_activations"],
        )
        return global_outs

