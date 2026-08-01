
def _swap_modules(
    ep: ExportedProgram, modules_to_swap: dict[str, torch.nn.Module]
) -> torch.fx.GraphModule:
    """
    Unlifts the given ExportedProgram into a fx.GraphModule, and then swaps
    previously traced modules with new eager modules specified. Returns a
    fx.GraphModule with a custom forward function.

    Args:
        ep (ExportedProgram): Exported program to modify
        modules_to_swap (Dict[str, torch.nn.Module]): Mapping from module fqn to
            eager module to swap with. The specified module fqn should have also
            been specified in the `preserve_module_call_signature` argument to
            torch.export so that we know how to restore the calling convention
            to this argument.
        run_with_interpreter: Whether or not to run the graph using
            fx.Interpreter. Setting to true will help result in better error
            messages and easier debugging, but it has found to result in a QPS
            drop.
    """
    module_call_graph = {
        entry.fqn: entry.signature for entry in ep.module_call_graph if entry.signature
    }

    gm = ep.module()
    gm.validate_inputs = False  # type: ignore[assignment]
    gm.graph.eliminate_dead_code()  # type: ignore[operator, union-attr]
    if not isinstance(gm, torch.fx.GraphModule):
        raise AssertionError(
            f"Expected gm to be a torch.fx.GraphModule, but got {type(gm)}"
        )
    _fix_input_output_signature(gm, ep.module_call_graph[0].signature)

    gm.module_call_graph = ep.module_call_graph
    gm.train = types.MethodType(type(gm).train, gm)  # type: ignore[assignment]
    gm.eval = types.MethodType(type(gm).eval, gm)  # type: ignore[assignment]

    if not isinstance(gm, torch.fx.GraphModule):
        raise AssertionError(
            f"Expected gm to be a torch.fx.GraphModule, but got {type(gm)}"
        )
    gm = _swap_module_helper(gm, modules_to_swap, module_call_graph)

    return gm

