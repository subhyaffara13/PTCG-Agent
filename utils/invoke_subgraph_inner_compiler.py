
def invoke_subgraph_inner_compiler(
    subgraph: torch.fx.GraphModule, example_inputs: list[torch.Tensor]
) -> Callable[..., Any]:
    """Inner compiler that wraps forward/backward graphs in invoke_subgraph HOP.

    This is used as the fw_compiler/bw_compiler for aot_autograd. When the resulting
    function is traced by make_fx, it emits an invoke_subgraph HOP instead of inlining.
    """
    from torch._dynamo import disable
    from torch._higher_order_ops.invoke_subgraph import invoke_subgraph_infer

    @disable
    # pyrefly: ignore [deprecated]
    @torch._dynamo.allow_in_graph
    def invoke_subgraph_wrapper_unboxed(*operands: Any) -> Any:
        return invoke_subgraph_infer(subgraph, *operands)

    # NB: The direct to unboxed path is broken, you MUST DO THIS

    def invoke_subgraph_wrapper(args: list[Any]) -> Any:
        return invoke_subgraph_wrapper_unboxed(*args)

    invoke_subgraph_wrapper._boxed_call = True  # type: ignore[attr-defined]

    return invoke_subgraph_wrapper

