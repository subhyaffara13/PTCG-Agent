
def _run_symbolic_method(g, op_name, symbolic_fn, args):
    r"""
    This trampoline function gets invoked for every symbolic method
    call from C++.
    """
    try:
        graph_context = jit_utils.GraphContext(
            graph=g,
            block=g.block(),
            opset=GLOBALS.export_onnx_opset_version,
            original_node=None,  # type: ignore[arg-type]
            params_dict=_params_dict,
            env={},
            values_in_env=set(),
            new_nodes=[],
        )
        return symbolic_fn(graph_context, *args)
    except TypeError as e:
        # Handle the specific case where we didn't successfully dispatch
        # to symbolic_fn.  Otherwise, the backtrace will have the clues
        # you need.
        e.args = (f"{e.args[0]} (occurred when translating {op_name})",)
        raise

