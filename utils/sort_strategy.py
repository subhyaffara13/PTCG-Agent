
def sort_strategy(op_schema: OpSchema, sort_dim: int) -> OpStrategy:
    input_strategy = cast(OpStrategy, op_schema.args_schema[0])
    sort_dim = normalize_dim(sort_dim, input_strategy.ndim)
    single_mesh_dim_strategies = []
    all_replicate: PlacementList = [Replicate()] * 3
    single_mesh_dim_strategies.append(all_replicate)
    for dim in range(input_strategy.ndim):
        if dim != sort_dim:
            dim_shardings: PlacementList = [Shard(dim)] * 3
            single_mesh_dim_strategies.append(dim_shardings)
    return expand_to_full_mesh_op_strategy(
        input_strategy.mesh, op_schema, single_mesh_dim_strategies, input_index=2
    )

