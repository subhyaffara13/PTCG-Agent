
def _insert_aten_to_metadata_assert_pass(gm: torch.fx.GraphModule) -> None:
    from torch._export.passes._node_metadata_hook import (
        _node_metadata_hook,
        _set_node_metadata_hook,
    )

    if _DISABLE_ATEN_TO_ASSERTION_PASS:
        return

    aten_to_variants = [
        torch.ops.aten.to.device,
        torch.ops.aten.to.dtype,
        torch.ops.aten.to.dtype_layout,
    ]
    for node in gm.graph.nodes:
        if node.target in aten_to_variants:
            if (
                node.prev.target is torch.ops.aten._assert_tensor_metadata.default
                and node.args[0] == node.prev.args[0]
            ):
                # skip if already guarded
                continue

            if (tensor_val := node.args[0].meta.get("val")) is not None:
                with (
                    gm.graph.inserting_before(node),
                    _set_node_metadata_hook(
                        gm,
                        functools.partial(
                            _node_metadata_hook,
                            metadata={
                                "stack_trace": node.meta.get("stack_trace"),
                                "nn_module_stack": node.meta.get("nn_module_stack"),
                            },
                        ),
                    ),
                ):
                    gm.graph.call_function(
                        torch.ops.aten._assert_tensor_metadata.default,
                        args=(node.args[0],),
                        kwargs={
                            "dtype": tensor_val.dtype,
                            "device": tensor_val.device,
                            "layout": tensor_val.layout,
                        },
                    )

