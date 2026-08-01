
def is_codegen_graph_partition_subgraph(wrapper: PythonWrapperCodegen) -> bool:
    from torch._inductor.codegen.wrapper import SubgraphPythonWrapperCodegen

    return (
        isinstance(wrapper, SubgraphPythonWrapperCodegen)
        and wrapper.partition_signatures is not None
    )

