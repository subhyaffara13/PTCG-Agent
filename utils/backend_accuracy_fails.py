
def backend_accuracy_fails(
    gm: torch.fx.GraphModule,
    example_inputs: Sequence[Any],
    compiler_fn: Callable[[torch.fx.GraphModule, list[Any]], torch.fx.GraphModule],
    only_fwd: bool = False,
    *,
    require_fp64: bool = False,
    ignore_non_fp: bool = False,
) -> bool:
    try:
        compiled_gm = compiler_fn(
            copy.deepcopy(gm), clone_inputs_retaining_gradness(example_inputs)
        )
        return not same_two_models(
            gm,
            compiled_gm,
            example_inputs,
            only_fwd,
            require_fp64=require_fp64,
            ignore_non_fp=ignore_non_fp,
        )
    except Exception:
        # This means that the minified graph is bad/exposes a different problem.
        # As we are checking accuracy here, lets log the exception and return False.
        log.exception(
            "While minifying the program in accuracy minification mode, "
            "ran into a runtime exception which is likely an unrelated issue."
            " Skipping this graph"
        )
        return False

