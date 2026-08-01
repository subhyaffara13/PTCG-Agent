
def replicate_op_strategy(op_schema: OpSchema) -> StrategyType:
    """
    Fallback strategy all use Replication()
    """
    args_strategy = op_schema.args_strategy
    kwargs_strategy = op_schema.kwargs_strategy
    inputs_strategy = args_strategy + kwargs_strategy

    output_type = [str(ret.type) for ret in op_schema.op._schema.returns]
    output_len = output_type.count("Tensor")
    # TODO(zpcore): Confirm if view op can be handle properly or not. Prevent
    # handling view ops until confirmed.
    if op_schema.op.is_view:
        raise RuntimeError(
            "fallback strategy is unable to handle view ops until confirmed"
        )
    if "List[Tensor]" in output_type:
        raise RuntimeError(
            "fallback strategy is unable to handle ops with List[Tensor] output "
            "because size of the list may depend on the op's input value"
        )

    mesh = inputs_strategy[0].mesh

    dim_sharding: PlacementList = [Replicate()] * (output_len + len(inputs_strategy))
    single_dim_placement = [dim_sharding]
    return expand_to_full_mesh_op_strategy(
        mesh, op_schema, single_dim_placement, input_index=output_len
    )

