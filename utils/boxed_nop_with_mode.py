
def boxed_nop_with_mode(
    fx_g: torch.fx.GraphModule,
    example_inputs: list[torch.Tensor],
    *,
    mode: torch.overrides.TorchFunctionMode,
) -> Callable[..., Any]:
    from torch.fx.graph import _BoxedCodeGen

    # Set the graph to use boxed codegen
    fx_g.graph.set_codegen(_BoxedCodeGen())
    fx_g.recompile()

    # Create a wrapper that runs with the mode
    forward_fn = fx_g.forward

    def run(args: Any) -> Any:
        with mode:
            return forward_fn(args)

    run._boxed_call = True  # type: ignore[attr-defined]
    return run

