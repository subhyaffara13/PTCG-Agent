
def embedding_dense_backward_strategy(op_schema: OpSchema) -> StrategyType:
    """
    This strategy handles embedding op. We have two possible embedding shardings:
    rowwise and colwise
    """
    grad_out_strategy = cast(OpStrategy, op_schema.args_schema[0])
    indices_strategy = cast(OpStrategy, op_schema.args_schema[1])
    mesh = op_schema.get_mesh_from_args()

    grad_out_shape = grad_out_strategy.shape
    indices_shape = indices_strategy.shape
    grad_out_ndim = len(grad_out_shape)

    single_mesh_dim_strategies = []

    # placement list stores placements of [output, weight, input_indices]
    # first we always have replicate all for inputs and output
    all_replicate: PlacementList = [Replicate()] * 3
    single_mesh_dim_strategies.append(all_replicate)

    # colwise sharding backward, grad_out shard on last dim, input replicate,
    # weight grad shard colwise
    colwise_sharding: PlacementList = [Shard(1), Shard(grad_out_ndim - 1), Replicate()]
    single_mesh_dim_strategies.append(colwise_sharding)

    # batch dim sharding, weight replicated, grad_out/input have same sharding
    # that can shard on any dim, weight grad partial
    for input_dim in range(len(indices_shape)):
        batch_sharding: PlacementList = [Partial(), Shard(input_dim), Shard(input_dim)]
        single_mesh_dim_strategies.append(batch_sharding)

    # grad_out partial, input replicate, weight grad keep partial
    partial_sharding: PlacementList = [Partial(), Partial(), Replicate()]
    single_mesh_dim_strategies.append(partial_sharding)

    return expand_to_full_mesh_op_strategy(mesh, op_schema, single_mesh_dim_strategies)

