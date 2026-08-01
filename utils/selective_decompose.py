
def selective_decompose(
    joint_gm: fx.GraphModule,
    *args: object,
    decomposition: Mapping[OpOverload, Callable[..., Any]] | None,
    should_decompose: Callable[..., bool],
    trace_joint_graph: bool,
) -> fx.GraphModule:
    """Retrace a joint graph module and selectively apply decomposition."""

    if trace_joint_graph:
        # the arg name, primals and tangents, are important.
        # make_fx keeps the name in the traced graph and partitioner later relies
        # on the name to partition joint graph correctly.
        def wrap_fn(primals: list[Any], tangents: list[Any]) -> Any:
            return _SelectiveDecomposeInterpreter.recursive_wrap(
                joint_gm, should_decompose, decomposition
            ).run(*args)
    else:

        def wrap_fn(*args: Any) -> Any:
            return _SelectiveDecomposeInterpreter.recursive_wrap(
                joint_gm, should_decompose, decomposition
            ).run(*args)

    return make_fx(wrap_fn, decomposition_table={})(*args)

