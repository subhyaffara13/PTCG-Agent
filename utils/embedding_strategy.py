
def embedding_strategy(op_schema: OpSchema) -> StrategyType:
    """
    This strategy handles embedding op. We have two possible embedding shardings:
    rowwise and colwise
    """
    weight_strategy = cast(OpStrategy, op_schema.args_schema[0])
    indices_strategy = cast(OpStrategy, op_schema.args_schema[1])
    mesh = op_schema.get_mesh_from_args()

    weight_shape = weight_strategy.shape
    indices_shape = indices_strategy.shape
    output_emd_dim = len(indices_shape)

    single_mesh_dim_strategies = []

    # placement list stores placements of [output, weight, input_indices]
    # first we always have replicate all for inputs and output
    all_replicate: PlacementList = [Replicate()] * 3
    single_mesh_dim_strategies.append(all_replicate)

    # colwise sharding, output shard on last dim, weight shard on dim 1, input replicate
    colwise_sharding: PlacementList = [Shard(output_emd_dim), Shard(1), Replicate()]
    single_mesh_dim_strategies.append(colwise_sharding)

    # rowwise sharding, output is embedding partial, weight shard on dim 0, input accepts embedding partial
    embedding_partial_placement = _MaskPartial(offset_shape=weight_shape, offset_dim=0)

    # NOTE we want to reuse the same mask partial placement so that we can reuse the same mask that generates
    # from the input indices and use it for output reduction
    rowwise_sharding: PlacementList = [
        embedding_partial_placement,
        Shard(0),
        embedding_partial_placement,
    ]
    single_mesh_dim_strategies.append(rowwise_sharding)

    # batch dim sharding, weight replicated, input can shard on any dim, output follows input
    for input_dim in range(len(indices_shape)):
        batch_sharding: PlacementList = [
            Shard(input_dim),
            Replicate(),
            Shard(input_dim),
        ]
        single_mesh_dim_strategies.append(batch_sharding)

    return expand_to_full_mesh_op_strategy(mesh, op_schema, single_mesh_dim_strategies)

