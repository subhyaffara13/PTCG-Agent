
def handle_dynamo_export_graph(
    gm: GraphModule,
    inputs: Sequence[InputType],
    compile_gm: Callable[..., Any],
) -> Callable[..., Any]:
    """
    `torch._dynamo.export` embeds pytrees in the FX graph codegen object,
    convert that to a normal FX graph so inductor can compile it.
    """
    codegen = gm.graph._codegen
    gm.graph._codegen = torch.fx.graph.CodeGen()
    gm.recompile()

    compiled_fn = compile_gm(gm, codegen.process_inputs(*inputs))

    @functools.wraps(compiled_fn)  # type: ignore[misc]
    def wrapper(*args: Any) -> Any:
        return codegen.process_outputs(compiled_fn(*codegen.process_inputs(*args)))

    return wrapper

