
def move_constructors_to_gpu(graph: fx.Graph) -> None:
    """
    Moves intermediary tensors which are constructed on the cpu to gpu when safe
    """

    # cudagraph does not support cpu tensors. In this pass, we update the graph
    # by explicitly moving cpu scalar tensors to gpu when profitable, relying on
    # graph partition to split off this data copy, and cudagraphifying
    # the remaining gpu ops.
    allow_inputs_outputs = bool(
        torch._inductor.config.triton.cudagraphs
        and torch._inductor.config.graph_partition
    )
    ConstructorMoverPass(
        get_gpu_type(),
        allow_inputs=allow_inputs_outputs,
        allow_outputs=allow_inputs_outputs,
    )(graph)

