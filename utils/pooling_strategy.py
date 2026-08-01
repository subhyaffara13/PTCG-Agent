
def pooling_strategy(op_schema: OpSchema) -> OpStrategy:
    input_strategy = cast(OpStrategy, op_schema.args_schema[0])
    mesh = input_strategy.mesh
    num_outputs = 2 if op_schema.op in MAX_POOL_OPS else 1
    num_inputs = len(op_schema.args_strategy) + len(op_schema.kwargs_strategy)
    n = num_outputs + num_inputs
    single_mesh_dim_strategies: list[PlacementList] = [
        [Replicate()] * n,
        [Shard(0)] * n,
    ]
    # avg_pool is linear: Partial(sum) and Partial(avg) pass through unchanged.
    if op_schema.op in AVG_POOL_OPS:
        single_mesh_dim_strategies.append([Partial("sum")] * n)
        single_mesh_dim_strategies.append([Partial("avg")] * n)
    # S(1) is safe when dim 1 is the channel dim (pooling never touches it).
    # Batched inputs have layout (N, C, *spatial) with ndim = spatial_rank + 2.
    spatial_rank = POOL_SPATIAL_RANK[op_schema.op]
    is_batched = input_strategy.ndim >= spatial_rank + 2
    if is_batched:
        single_mesh_dim_strategies.append([Shard(1)] * n)
    return expand_to_full_mesh_op_strategy(
        mesh, op_schema, single_mesh_dim_strategies, input_index=num_outputs
    )

