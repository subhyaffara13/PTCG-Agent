
def fake_crossref_boxed_nop(
    fx_g: torch.fx.GraphModule,
    example_inputs: list[torch.Tensor],
    ignore_op_fn: Callable[[torch._ops.OpOverload], bool] | None = None,
) -> Callable[..., Any]:
    from torch.fx.graph import _BoxedCodeGen

    # Set the graph to use boxed codegen
    fx_g.graph.set_codegen(_BoxedCodeGen())
    fx_g.recompile()

    # Create a wrapper that runs with the mode
    forward_fn = fx_g.forward

    def run(args: Any) -> Any:
        with torch._subclasses.CrossRefFakeMode(ignore_op_fn):
            return forward_fn(args)

    run._boxed_call = True  # type: ignore[attr-defined]
    return run

