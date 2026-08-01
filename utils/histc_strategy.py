
def histc_strategy(op_schema: OpSchema) -> OpStrategy:
    input_strategy = cast(OpStrategy, op_schema.args_schema[0])
    single_mesh_dim_strategies: list[PlacementList] = []
    single_mesh_dim_strategies.append([Replicate(), Replicate()])

    # histc can support sharded input and partial output on any input dim, provided the min and max
    # values are user-specified.  If not user-specified, the true min and max of the data in each local
    # tensor will be used to compute bin boundaries, which will not be the same across ranks, leading to
    # an incorrect final result
    if len(op_schema.args_schema) == 4:
        for dim in range(input_strategy.ndim):
            dim_shardings: PlacementList = [Partial(), Shard(dim)]
            single_mesh_dim_strategies.append(dim_shardings)

    return expand_to_full_mesh_op_strategy(
        input_strategy.mesh, op_schema, single_mesh_dim_strategies
    )

