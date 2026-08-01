
def apply_runtime_assertion_pass(gm: torch.fx.GraphModule, graph_signature):
    from torch._export.passes._node_metadata_hook import (
        _node_metadata_hook,
        _set_node_metadata_hook,
    )
    from torch._functorch._aot_autograd.input_output_analysis import _graph_output_names

    if not torch._dynamo.config.do_not_emit_runtime_asserts:
        stack_trace = (
            'File "torch/fx/passes/runtime_assert.py", line 24, '
            "in insert_deferred_runtime_asserts"
        )
        with _set_node_metadata_hook(
            gm,
            functools.partial(
                _node_metadata_hook, metadata={"stack_trace": stack_trace}
            ),
        ):
            shape_env = _get_shape_env_from_gm(gm)
            if shape_env:
                insert_deferred_runtime_asserts(
                    gm,
                    shape_env,
                    f"exported program: {first_call_function_nn_module_stack(gm.graph)}",
                    export=True,
                )

        # insert runtime assertions for aten.to nodes
        _insert_aten_to_metadata_assert_pass(gm)

    # update output specs
    gm.recompile()
    graph_signature.user_outputs = _graph_output_names(gm)
    return gm, graph_signature

